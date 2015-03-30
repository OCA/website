# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class CrmTurnoverRange(models.Model):
    _name = 'crm.turnover_range'
    _description = "Turnover range"

    name = fields.Char(required=True, translate=True)
