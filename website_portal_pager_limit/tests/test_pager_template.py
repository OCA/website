# Copyright (C) 2026 XXP
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from .common import TestPortalPagerLimitCommon


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
