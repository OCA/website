# -*- coding: utf-8 -*-
#
#    Jamotion GmbH, Your Odoo implementation partner
#    Copyright (C) 2013-2015 Jamotion GmbH.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Created by angel.moya on 01.09.2016.
#
from openerp.tests import common


class TestWebsiteSaleSurvey(common.TransactionCase):

    def setUp(self):
        super(TestWebsiteSaleSurvey, self).setUp()
        self.data = self.env['ir.model.data']

        self.survey_id = self.data.xmlid_to_res_id(
            'survey.feedback_form')
        self.survey_obj = self.env['survey.survey']
        self.survey = self.survey_obj.browse(
            self.survey_id)

        self.sale_order_id = self.data.xmlid_to_res_id(
            'sale.sale_order_1')
        self.sale_order_obj = self.env['sale.order']
        self.sale_order = self.sale_order_obj.browse(
            self.sale_order_id)

    def test_01_not_default_survey(self):
        self.assertFalse(self.sale_order.survey_id.id)

    def test_02_set_default_survey(self):
        self.survey.default_for_website_sales = True
        self.assertEqual(
            self.sale_order.survey_id,
            self.survey)
        self.survey_2 = self.survey.copy({'default_for_website_sales': False})
        catch_validate_error = False
        try:
            self.survey_2.write({'default_for_website_sales': True})
        except:
            catch_validate_error = True
        self.assertTrue(catch_validate_error)
