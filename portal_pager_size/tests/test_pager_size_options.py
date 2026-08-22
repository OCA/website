# Copyright (C) 2026 XXP
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.portal_pager_size.controllers.portal import (
    DEFAULT_SIZE_OPTIONS,
    OPTIONS_PARAM,
)

from .common import TestPortalPagerSizeCommon


class TestPagerSizeOptions(TestPortalPagerSizeCommon):
    def test_options_canonical_value(self):
        """A well formed parameter is parsed into the whitelist."""
        self._set_options_param("10,20,40,80,100")
        with self._mock_request():
            self.assertEqual(
                self.controller._get_portal_pager_size_options(),
                [10, 20, 40, 80, 100],
            )

    def test_options_custom_param(self):
        self._set_options_param(" 5, 15,25 ")
        with self._mock_request():
            self.assertEqual(
                self.controller._get_portal_pager_size_options(), [5, 15, 25]
            )

    def test_options_partial_garbage(self):
        """Non numeric entries are discarded, valid ones are kept."""
        self._set_options_param("abc, 15, -5, 12.5, 30, ")
        with self._mock_request():
            self.assertEqual(self.controller._get_portal_pager_size_options(), [15, 30])

    def test_options_full_garbage_falls_back(self):
        """A fully broken parameter can not disable the pagination."""
        self._set_options_param("abc, foo; bar")
        with self._mock_request():
            self.assertEqual(
                self.controller._get_portal_pager_size_options(),
                list(DEFAULT_SIZE_OPTIONS),
            )

    def test_options_missing_param(self):
        """Without the parameter the hardcoded default applies."""
        self.env["ir.config_parameter"].sudo().search(
            [("key", "=", OPTIONS_PARAM)]
        ).unlink()
        with self._mock_request():
            self.assertEqual(
                self.controller._get_portal_pager_size_options(),
                list(DEFAULT_SIZE_OPTIONS),
            )
