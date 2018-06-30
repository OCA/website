# -*- coding: utf-8 -*-#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestWebsiteVersionBase(common.TransactionCase):

    def setUp(self):
        super(TestWebsiteVersionBase, self).setUp()

        # Useful models
        self.orm_view = self.env['ir.ui.view']
        self.orm_version = self.env['website_version_ce.version']
        ir_model_data_reg = self.env["ir.model.data"]

        # Useful objects
        master_view = ir_model_data_reg.xmlid_to_object(
            'website.website2_homepage')
        self.arch_master = master_view.arch
        self.version = ir_model_data_reg.xmlid_to_object(
            'website_version_ce.version_0_0_0_0')
        self.website = ir_model_data_reg.xmlid_to_object(
            'website.website2')
        self.view_0_0_0_0 = ir_model_data_reg.xmlid_to_object(
            'website_version_ce.website2_homepage_other')
        self.arch_0_0_0_0 = self.view_0_0_0_0.arch
