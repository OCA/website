# Copyright (C) 2026 XXP
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from contextlib import contextmanager
from types import SimpleNamespace

from odoo.http import _request_stack
from odoo.tests.common import HttpCase, TransactionCase, tagged

from odoo.addons.website_portal_pager_limit.controllers.portal import (
    DEFAULT_LIMIT_OPTIONS,
    OPTIONS_PARAM,
    CustomerPortal,
)

STANDARD_LIMIT = 80


class TestPortalPagerLimitCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = CustomerPortal()
        cls.portal_user = (
            cls.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": "Portal Pager User",
                    "login": "portal_pager_user",
                    "email": "portal_pager_user@example.com",
                    "groups_id": [(6, 0, [cls.env.ref("base.group_portal").id])],
                }
            )
        )

    def _set_options_param(self, value):
        self.env["ir.config_parameter"].sudo().set_param(OPTIONS_PARAM, value)

    @contextmanager
    def _mock_request(self, args=None, env=None):
        """Expose a minimal fake request through the odoo.http proxy.

        Both this module's controller and the base portal controller read
        the same ``request`` local stack proxy, so pushing a lightweight
        object is enough to exercise the request-bound code paths.
        """
        fake_request = SimpleNamespace(
            env=env or self.env,
            httprequest=SimpleNamespace(args=args or {}),
        )
        _request_stack.push(fake_request)
        try:
            yield fake_request
        finally:
            _request_stack.pop()


class TestPagerLimitOptions(TestPortalPagerLimitCommon):
    def test_options_from_module_data(self):
        """The shipped system parameter is parsed into the whitelist."""
        with self._mock_request():
            self.assertEqual(
                self.controller._get_portal_pager_limit_options(),
                [10, 20, 40, 80, 100],
            )

    def test_options_custom_param(self):
        self._set_options_param(" 5, 15,25 ")
        with self._mock_request():
            self.assertEqual(
                self.controller._get_portal_pager_limit_options(), [5, 15, 25]
            )

    def test_options_partial_garbage(self):
        """Non numeric entries are discarded, valid ones are kept."""
        self._set_options_param("abc, 15, -5, 12.5, 30, ")
        with self._mock_request():
            self.assertEqual(
                self.controller._get_portal_pager_limit_options(), [15, 30]
            )

    def test_options_full_garbage_falls_back(self):
        """A fully broken parameter can not disable the pagination."""
        self._set_options_param("abc, foo; bar")
        with self._mock_request():
            self.assertEqual(
                self.controller._get_portal_pager_limit_options(),
                DEFAULT_LIMIT_OPTIONS,
            )

    def test_options_missing_param(self):
        """Without the parameter the hardcoded default applies."""
        self.env["ir.config_parameter"].sudo().search(
            [("key", "=", OPTIONS_PARAM)]
        ).unlink()
        with self._mock_request():
            self.assertEqual(
                self.controller._get_portal_pager_limit_options(),
                DEFAULT_LIMIT_OPTIONS,
            )


class TestItemsPerPage(TestPortalPagerLimitCommon):
    def test_valid_limit(self):
        with self._mock_request(args={"limit": "20"}):
            self.assertEqual(self.controller._items_per_page, 20)

    def test_limit_not_whitelisted(self):
        """Arbitrary high values are rejected to avoid huge queries."""
        with self._mock_request(args={"limit": "999999"}):
            self.assertEqual(self.controller._items_per_page, STANDARD_LIMIT)

    def test_limit_non_numeric(self):
        for bad_value in ("abc", "-5", "12.5", ""):
            with self._mock_request(args={"limit": bad_value}):
                self.assertEqual(
                    self.controller._items_per_page,
                    STANDARD_LIMIT,
                    "limit=%r must fall back to the default" % bad_value,
                )

    def test_limit_missing(self):
        with self._mock_request():
            self.assertEqual(self.controller._items_per_page, STANDARD_LIMIT)

    def test_limit_with_custom_options(self):
        self._set_options_param("5,15")
        with self._mock_request(args={"limit": "15"}):
            self.assertEqual(self.controller._items_per_page, 15)
        # 20 is valid in the default whitelist but not in the custom one
        with self._mock_request(args={"limit": "20"}):
            self.assertEqual(self.controller._items_per_page, STANDARD_LIMIT)

    def test_portal_layout_values(self):
        """Portal rendering context exposes the options and current limit."""
        portal_env = self.env(user=self.portal_user)
        with self._mock_request(args={"limit": "20"}, env=portal_env):
            values = self.controller._prepare_portal_layout_values()
        self.assertEqual(values["portal_pager_limit_options"], [10, 20, 40, 80, 100])
        self.assertEqual(values["portal_pager_limit"], 20)


class TestPagerTemplate(TestPortalPagerLimitCommon):
    def _render_pager(self, values=None):
        pager = {
            "page_count": 2,
            "offset": 0,
            "page": {"url": "/my/orders", "num": 1},
            "page_first": {"url": "/my/orders", "num": 1},
            "page_start": {"url": "/my/orders", "num": 1},
            "page_previous": {"url": "/my/orders", "num": 1},
            "page_next": {"url": "/my/orders/page/2", "num": 2},
            "page_end": {"url": "/my/orders/page/2", "num": 2},
            "page_last": {"url": "/my/orders/page/2", "num": 2},
            "pages": [
                {"url": "/my/orders", "num": 1},
                {"url": "/my/orders/page/2", "num": 2},
            ],
        }
        return str(
            self.env["ir.qweb"]._render("portal.pager", dict(values or {}, pager=pager))
        )

    def test_selector_rendered_with_options(self):
        html = self._render_pager(
            {
                "portal_pager_limit_options": [10, 20, 40, 80, 100],
                "portal_pager_limit": 20,
            }
        )
        self.assertIn("o_portal_pager_limit", html)
        self.assertIn('<option value="20" selected="selected">20</option>', html)
        self.assertIn('<option value="100">100</option>', html)

    def test_selector_not_rendered_without_options(self):
        """Third party callers of portal.pager without our context keep
        working and simply do not get the selector."""
        html = self._render_pager()
        self.assertNotIn("o_portal_pager_limit", html)


@tagged("post_install", "-at_install")
class TestPortalPagerLimitHttp(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.users"].with_context(no_reset_password=True).create(
            {
                "name": "Portal Pager Http User",
                "login": "portal_pager_http_user",
                "email": "portal_pager_http_user@example.com",
                "password": "portal_pager_http_user",
                "groups_id": [(6, 0, [cls.env.ref("base.group_portal").id])],
            }
        )

    def test_portal_pages_accept_limit_param(self):
        """Portal routes must not crash, whatever the limit value is."""
        self.authenticate("portal_pager_http_user", "portal_pager_http_user")
        for query in ("limit=20", "limit=999999", "limit=abc"):
            response = self.url_open("/my?%s" % query)
            self.assertEqual(
                response.status_code,
                200,
                "/my?%s must render fine" % query,
            )
