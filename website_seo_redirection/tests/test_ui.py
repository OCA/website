# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests.common import HttpCase


class UICase(HttpCase):
    def test_admin_tour_en_US(self):
        """Redirections work with default language."""
        tour = "odoo.__DEBUG__.services['web.Tour']"
        self.phantom_js(
            "/en_US",
            tour + ".run('website_seo_redirection')",
            tour + ".tours.website_seo_redirection",
        )
