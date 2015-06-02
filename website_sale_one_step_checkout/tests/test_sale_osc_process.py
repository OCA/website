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
import openerp.tests

# Test onstepcheckout


@openerp.tests.common.at_install(False)
@openerp.tests.common.post_install(True)
class TestUi(openerp.tests.HttpCase):
    def test_01_admin_checkout(self):
        self.phantom_js("/", "openerp.Tour.run('shop_buy_product_osc',"
                             "" "'test')",
                        "openerp.Tour.tours.shop_buy_product_osc",
                        login="admin")

    def test_02_demo_checkout(self):
        self.phantom_js("/", "openerp.Tour.run('shop_buy_product_osc', "
                             "'test')",
                        "openerp.Tour.tours.shop_buy_product_osc",
                        login="demo")

    def test_03_public_checkout(self):
        self.phantom_js("/", "openerp.Tour.run('shop_buy_product_osc', "
                             "'test')",
                        "openerp.Tour.tours.shop_buy_product_osc")
