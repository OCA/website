# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests.common import HttpCase


class UICase(HttpCase):
    def test_ui_website_portal_product_manager(self):
        """Test frontend tour."""
        # See https://github.com/odoo/odoo/pull/13902
        with self.cursor() as cr:
            # TODO Remove all this and use Demo Portal User after merging
            # https://github.com/odoo/odoo/pull/14777
            env = self.env(cr)
            # Set demo user as a portal user
            env.ref("base.user_demo").groups_id = env.ref("base.group_portal")

        self.phantom_js(
            url_path="/",
            code="odoo.__DEBUG__.services['web.Tour']"
                 ".run('website_portal_purchase_product_tour', 'test')",
            ready="odoo.__DEBUG__.services['web.Tour'].tours"
                  ".website_portal_purchase_product_tour",
            login="demo")
