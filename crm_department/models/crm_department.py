# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class CrmDepartment(models.Model):
    _name = 'crm.department'
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "Department"

    name = fields.Char(required=True, translate=True)
    parent_id = fields.Many2one(comodel_name='crm.department')
    children = fields.One2many(comodel_name='crm.department',
                               inverse_name='parent_id')
    parent_left = fields.Integer('Parent Left', select=True)
    parent_right = fields.Integer('Parent Right', select=True)
