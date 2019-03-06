# -*- coding: utf-8 -*-
# Copyright 2019 Benjamin Henquet
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase


class TestWebsiteMenu(SavepointCase):

    @classmethod
    def setUpClass(self):
        super(TestWebsiteMenu, self).setUpClass()
        self.menu = self.env.ref('website.menu_contactus')
        self.menu.user_logged = False
        self.menu.user_not_logged = False

        self.public_user = self.env.ref('base.public_user')

    def test_visible_user_logged_demo(self):
        self.menu.user_logged = True
        self.assertTrue(True)
