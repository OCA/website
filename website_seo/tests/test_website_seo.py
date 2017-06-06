# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, an open source suite of business apps
# This module copyright (C) 2015 bloopark systems (<http://bloopark.de>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.exceptions import ValidationError
from openerp.tests import common


class TestWebsiteSeo(common.TransactionCase):

    """Unit tests about website SEO url validation."""

    at_install = False
    post_install = True

    def test_00_website_seo(self):
        """----- Test valid SEO url."""
        self.assertTrue(self.env['website.seo.metadata'].
                        validate_seo_url('my-blog-post'))

    def test_01_website_seo(self):
        """----- Test invalid SEO url."""
        with self.assertRaises(ValidationError):
            self.env['website.seo.metadata'].validate_seo_url('my-blog-post!')
