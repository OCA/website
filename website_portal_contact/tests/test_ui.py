# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import odoo.tests


@odoo.tests.tagged('post_install', '-at_install')
class TestUi(odoo.tests.HttpCase):
    def test_01_demo_contact_tour(self):
        self.phantom_js(url_path="/",
                        code="odoo.__DEBUG__.services['web_tour.tour']"
                             ".run('test_website_portal_contact')",
                        ready="odoo.__DEBUG__.services['web_tour.tour']"
                              ".tours.test_website_portal_contact.ready",
                        login="demo")
