# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import odoo.tests


class TestUi(odoo.tests.HttpCase):
    def test_01_portal_contact_test_tour(self):
        self.start_tour("/", "portal_contacts", login="portal")
