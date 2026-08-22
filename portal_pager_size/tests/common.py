# Copyright (C) 2026 XXP
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from contextlib import contextmanager
from types import SimpleNamespace

from odoo.http import _request_stack
from odoo.tests.common import TransactionCase

from odoo.addons.portal_pager_size.controllers.portal import (
    OPTIONS_PARAM,
    CustomerPortal,
)

STANDARD_LIMIT = 80


class TestPortalPagerSizeCommon(TransactionCase):
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
