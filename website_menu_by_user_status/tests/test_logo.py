# -*- coding: utf-8 -*-
# Copyright 2018 David Dufresne
# Copyright 2019 Benjamin Henquet
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase


class TestWebsiteMenu(SavepointCase):

    def setUp(self):
        super(TestWebsiteMenu, self).setUp()
        self.page = self.env.ref('website.contactus_page')
        self.page.is_visible = False

        self.menu = self.env.ref('website.menu_contactus')
        self.menu.user_logged = False
        self.menu.user_not_logged = False

        self.public_user = self.env.ref('base.public_user')
        self.demo_user = self.env.ref('base.user_demo')

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
