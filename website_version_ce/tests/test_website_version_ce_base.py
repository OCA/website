# -*- coding: utf-8 -*-#
# © 2016 Nicolas Petit <nicolas.petit@vivre-d-internet.fr>
# © 2016, TODAY Odoo S.A
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests import common


class TestWebsiteVersionBase(common.TransactionCase):

    def setUp(self):
        super(TestWebsiteVersionBase, self).setUp()
        cr, uid = self.cr, self.uid

        # Useful models
        self.orm_view = self.env['ir.ui.view']
        self.orm_version = self.env['website_version_ce.version']
        ir_model_data_reg = self.registry('ir.model.data')

        # Useful objects
        master_view = ir_model_data_reg.xmlid_to_object(
            cr, uid, 'website.website2_homepage', context=None)
        self.arch_master = master_view.arch
        self.version = ir_model_data_reg.xmlid_to_object(
            cr, uid, 'website_version_ce.version_0_0_0_0', context=None)
        self.website = ir_model_data_reg.xmlid_to_object(
            cr, uid, 'website.website2', context=None)
        self.view_0_0_0_0 = ir_model_data_reg.xmlid_to_object(
            cr, uid, 'website_version_ce.website2_homepage_other',
            context=None)
        self.arch_0_0_0_0 = self.view_0_0_0_0.arch
