# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class CrmEmployeesRange(models.Model):
    _name = 'crm.employees_range'
    _description = "Employees range"

    name = fields.Char(required=True, translate=True)
