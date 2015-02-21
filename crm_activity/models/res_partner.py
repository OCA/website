# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    activity = fields.Many2one(comodel_name='crm.activity')
    activity_others = fields.Many2many(comodel_name='crm.activity',
                                       string="Other activities")
