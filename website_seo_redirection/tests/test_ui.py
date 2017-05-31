# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import HttpCase


class UICase(HttpCase):

    post_install = True
    at_install = False

    def test_admin_tour_en_US(self):
        """Redirections work with default language."""
        tour = "odoo.__DEBUG__.services['web_tour.tour']"
        self.phantom_js(
            "/en_US",
            "%s.run('website_seo_redirection')" % tour,
            "%s.tours.website_seo_redirection.ready" % tour,
        )
