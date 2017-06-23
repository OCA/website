# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import HttpCase


class UICase(HttpCase):

    post_install = True
    at_install = False

    def test_category_browse(self):
        """Redirections work with default language."""
        tour = "odoo.__DEBUG__.services['web_tour.tour']"
        self.phantom_js(
            "/blog/our-blog-1",
            "%s.run('website_blog_category')" % tour,
            "%s.tours.website_blog_category.ready" % tour,
            login="admin",
        )
