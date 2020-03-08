# Copyright 2019 Mathieu Benoit <mathieu.benoit@mathben.tech>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.tests


@odoo.tests.tagged('post_install', '-at_install')
class TestUi(odoo.tests.HttpCase):
    def test_01_demo_address_tour(self):
        self.phantom_js(url_path="/",
                        code="odoo.__DEBUG__.services['web_tour.tour']"
                             ".run('test_website_portal_address')",
                        ready="odoo.__DEBUG__.services['web_tour.tour']"
                              ".tours.test_website_portal_address.ready",
                        login="demo")
