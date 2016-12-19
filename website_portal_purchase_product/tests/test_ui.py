# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests.common import HttpCase


class UICase(HttpCase):
    def test_ui_website_portal_product_manager(self):
        """Test frontend tour."""
        self.parent = self.env["res.partner"].create({
            "name": "Tourman parent company",
            "is_company": True,
            "supplier": True,
        })
        self.tourman = self.env["res.users"].create({
            "name": "Tourman",
            "parent_id": self.parent,
            "login": "tourman",
            "new_password": "tourman",
            "groups_id":
                [(4, self.env.ref("base.group_portal").id, False)],
        })

        self.phantom_js(
            url_path="/",
            code="odoo.__DEBUG__.services['web.Tour']"
                 ".run('website_portal_purchase_product_tour', 'test')",
            ready="odoo.__DEBUG__.services['web.Tour'].tours"
                  ".website_portal_purchase_product_tour",
            login="tourman")
