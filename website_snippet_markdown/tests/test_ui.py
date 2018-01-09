# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import HttpCase


class UICase(HttpCase):
    def test_ui_website(self):
        tour = (
            "odoo.__DEBUG__.services['web_tour.tour']",
            "website_snippet_markdown.tour",
        )
        self.phantom_js(
            url_path="/",
            code="%s.run('%s')" % tour,
            ready="%s.tours['%s'].ready" % tour,
            login="admin"
        )
