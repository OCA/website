# -*- coding: utf-8 -*-
# Copyright 2016 Jamotion GmbH
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#    Created by angel.moya on 01.09.2016.
#
from openerp import models, api, fields, _
from openerp.exceptions import ValidationError


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    default_for_website_sales = fields.Boolean(
        string='Default for Website Sales',
        help='If checked this survey could be done by customer after payment, '
             'no more than one survey could be set as default.')

    @api.constrains('default_for_website_sales')
    def _check_field(self):
        defaults = self.search([('default_for_website_sales', '=', True)])
        if len(defaults) > 1:
            raise ValidationError(
                _("No more than one survey could be set as default."))


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order')
