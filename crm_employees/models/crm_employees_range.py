# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class CrmEmployeesRange(models.Model):
    _name = 'crm.employees_range'
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "Employees range"

    name = fields.Char(required=True)
    parent_id = fields.Many2one(comodel_name='crm.employees_range')
    children = fields.One2many(comodel_name='crm.employees_range',
                               inverse_name='parent_id')
    parent_left = fields.Integer('Parent Left', select=True)
    parent_right = fields.Integer('Parent Right', select=True)
