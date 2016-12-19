# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests.common import HttpCase


class UICase(HttpCase):
    def test_ui_website_portal_product_manager(self):
        """Test frontend tour."""
        # See https://github.com/odoo/odoo/pull/13902
        with self.cursor() as cr:
            env = self.env(cr)
            # Create a portal user to avoid dependency on portal module
            self.parent = env["res.partner"].create({
                "name": "Tourman parent company",
                "is_company": True,
                "supplier": True,
            })
            self.tourman = env["res.users"].create({
                "name": "Tourman",
                "parent_id": self.parent.id,
                "login": "tourman",
                "new_password": "tourman",
                "groups_id":
                    [(4, env.ref("base.group_portal").id, False)],
            })

        self.phantom_js(
            url_path="/",
            code="odoo.__DEBUG__.services['web.Tour']"
                 ".run('website_portal_purchase_product_tour', 'test')",
            ready="odoo.__DEBUG__.services['web.Tour'].tours"
                  ".website_portal_purchase_product_tour",
            login="tourman")
