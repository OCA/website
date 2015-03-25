# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    employees_range = fields.Many2one(comodel_name='crm.employees_range')
    employees_number = fields.Integer()
