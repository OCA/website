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
from openerp.tests import common


class TestWebsiteSwitcher(common.TransactionCase):

    """Testing class for module website_switcher."""

    at_install = False
    post_install = True

    def setUp(self):
        """Set up method."""
        super(TestWebsiteSwitcher, self).setUp()

    def test_01_website(self):
        """----- Test if select_websites are available in templates."""
        website_obj = self.env['website']

        website_obj.create({
            'domain': 'example.com',
            'name': 'example',
        })

        view = self.env['ir.ui.view'].create({
            'name': "Test View",
            'type': 'qweb',
            'arch': """<t t-foreach="portal_websites" t-as="select_websites">
<li><a t-att-href="'http://' + select_websites.domain">
<t t-esc="select_websites.name" /></a></li></t>""",
        })

        result = view.render()
        expected_result = []
        for website in website_obj.search([]):
            expected_result.append(
                '<li><a href="http://{}">{}</a></li>'.format(
                    website.domain, website.name))

        self.assertEqual(result.replace('\n', ''), ''.join(expected_result))
