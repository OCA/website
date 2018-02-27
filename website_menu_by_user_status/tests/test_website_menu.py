# Copyright 2018 David Dufresne
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase


class TestWebsiteMenu(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.page = cls.env.ref('website.contactus_page')
        cls.page.is_visible = False

        cls.menu = cls.env.ref('website.menu_contactus')
        cls.menu.user_logged = False
        cls.menu.user_not_logged = False

        cls.public_user = cls.env.ref('base.public_user')
        cls.demo_user = cls.env.ref('base.user_demo')

    def test_visible_user_logged_demo(self):
        self.page.is_visible = True
        self.menu.user_logged = True
        self.assertTrue(self.menu.sudo(self.demo_user).is_visible)

    def test_visible_user_logged_public(self):
        self.page.is_visible = True
        self.menu.user_logged = True
        self.assertFalse(self.menu.sudo(self.public_user).is_visible)

    def test_visible_user_not_logged_demo(self):
        self.page.is_visible = True
        self.user_not_logged = True
        self.assertFalse(self.menu.sudo(self.demo_user).is_visible)

    def test_visible_user_not_logged_public(self):
        self.page.is_visible = True
        self.user_not_logged = True
        self.assertFalse(self.menu.sudo(self.public_user).is_visible)

    def test_not_visible_user_logged_demo(self):
        self.menu.user_logged = True
        self.assertTrue(self.menu.sudo(self.demo_user).is_visible)

    def test_not_visible_user_logged_public(self):
        self.menu.user_logged = True
        self.assertFalse(self.menu.sudo(self.public_user).is_visible)

    def test_not_visible_user_not_logged_demo(self):
        self.user_not_logged = True
        self.assertFalse(self.menu.sudo(self.demo_user).is_visible)

    def test_not_visible_user_not_logged_public(self):
        self.user_not_logged = True
        self.assertFalse(self.menu.sudo(self.public_user).is_visible)
