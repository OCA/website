# Copyright (C) 2026 XXP
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from .common import STANDARD_LIMIT, TestPortalPagerLimitCommon


class TestItemsPerPage(TestPortalPagerLimitCommon):
    def test_valid_limit(self):
        self._set_options_param("10,20,40,80,100")
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
        self._set_options_param("10,20,40,80,100")
        portal_env = self.env(user=self.portal_user)
        with self._mock_request(args={"limit": "20"}, env=portal_env):
            values = self.controller._prepare_portal_layout_values()
        self.assertEqual(values["portal_pager_limit_options"], [10, 20, 40, 80, 100])
        self.assertEqual(values["portal_pager_limit"], 20)
