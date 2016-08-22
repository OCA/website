# -*- coding: utf-8 -*-
##############################################################################
#
# Authors: Odoo S.A., Nicolas Petit (Clouder)
# Copyright 2016, TODAY Odoo S.A. Clouder SASU
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tests import common


class TestWebsiteVersionBase(common.TransactionCase):

    def setUp(self):
        super(TestWebsiteVersionBase, self).setUp()
        cr, uid = self.cr, self.uid

        # Useful models
        self.ir_ui_view = self.env['ir.ui.view']
        self.website_version_version = self.env['website_version.version']
        self.website = self.env['website']
        self.ir_model_data = self.env['ir.model.data']

        # Useful objects
        master_view = self.registry('ir.model.data').xmlid_to_object(cr, uid, 'website.website2_homepage',
                                                                     context=None)
        self.arch_master = master_view.arch
        self.version = self.registry('ir.model.data').xmlid_to_object(cr, uid, 'website_version.version_0_0_0_0',
                                                                      context=None)
        self.website = self.registry('ir.model.data').xmlid_to_object(cr, uid, 'website.website2', context=None)
        self.view_0_0_0_0 = self.registry('ir.model.data').xmlid_to_object(cr, uid,
                                                                           'website_version.website2_homepage_other',
                                                                           context=None)
        self.arch_0_0_0_0 = self.view_0_0_0_0.arch
