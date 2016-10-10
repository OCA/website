# -*- coding: utf-8 -*-
# Copyright 2016 Jamotion GmbH
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#    Created by angel.moya on 01.09.2016.
#
from openerp import models, api, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    survey_id = fields.Many2one(
        comodel_name='survey.survey',
        string='Survey',
        compute='_compute_survey_id')

    @api.multi
    def _compute_survey_id(self):
        survey = self.env['survey.survey'].search(
            [('default_for_website_sales', '=', True)])
        survey = len(survey) > 0 and survey[0] or False
        for record in self:
            record.survey_id = survey
