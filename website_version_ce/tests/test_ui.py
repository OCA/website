# -*- coding: utf-8 -*-#
# © 2016 Nicolas Petit <nicolas.petit@vivre-d-internet.fr>
# © 2016, TODAY Odoo S.A
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import openerp.tests


@openerp.tests.common.at_install(False)
@openerp.tests.common.post_install(True)
class TestUi(openerp.tests.HttpCase):
    def test_01_versioning(self):
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web.Tour'].run('versioning', 'test')",
            "odoo.__DEBUG__.services['web.Tour'].tours.versioning",
            login='admin'
        )
