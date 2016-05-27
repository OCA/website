# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import HttpCase


class UICase(HttpCase):
    def test_ui_website(self):
        """Test frontend tour."""
        demo = self.env.ref("base.partner_demo")
        demo.customer = demo.supplier = True
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web.Tour']"
            ".run('test_website_portal_tabbed', 'test')",
            "odoo.__DEBUG__ices['web.Tour'].tours.test_website_portal_tabbed",
            "demo")
