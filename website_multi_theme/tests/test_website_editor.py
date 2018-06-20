# -*- coding: utf-8 -*-
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api
from odoo.tests.common import HttpCase


class WebsiteEditor(HttpCase):

    def test_snippets(self):
        """Check that there is no error after duplicating snippets."""
        env = api.Environment(self.registry.test_cr, self.uid, {})

        theme = env.ref('website_multi_theme.demo_multi')

        # apply same theme for different website, so to be sure that we have
        # more than one copy of snippet
        env.ref("website.default_website").multi_theme_id = theme
        env.ref("website.website2").multi_theme_id = theme
        env["res.config.settings"].multi_theme_reload()

        # run tour from module "website", where Edit button is clicked, so
        # snippets are loaded
        self.phantom_js(
            '/',

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('banner')",

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.banner.ready",

            login='admin'
        )
