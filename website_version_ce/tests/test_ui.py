# -*- coding: utf-8 -*-#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import odoo.tests


@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):
    def test_01_versioning(self):
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web_tour.tour'].run('versioning')",
            "odoo.__DEBUG__.services['web_tour.tour'].tours.versioning.ready",
            login='admin'
        )
