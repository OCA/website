# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import HttpCase, new_test_user, tagged


@tagged("-at_install", "post_install")
class TestConditionalVisibilityUserGroup(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        new_test_user(cls.env, login="portal_user", groups="base.group_portal")

    def test_snippet_for_internal_users(self):
        """Only internal users can see the snippet"""
        # We drag a new block, set its visibility to internal users and check that
        # we can see it as internal users
        self.start_tour("/", "conditional_visibility_only_internal_user", login="admin")
        # The block is hidden for portal users
        self.start_tour("/", "conditional_visibility_portal", login="portal_user")
