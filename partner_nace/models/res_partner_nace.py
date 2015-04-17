# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Antonio Espinosa <antonioea@antiun.com>
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
##############################################################################

from openerp import models, fields


class ResPartnerNace(models.Model):
    _name = 'res.partner.nace'
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "NACE Activity"

    # NACE fields
    level = fields.Integer(required=True)
    code = fields.Char(required=True)
    name = fields.Char(required=True, translate=True)
    generic = fields.Char(string="ISIC Rev.4")
    rules = fields.Text()
    central_content = fields.Text(translate=True, string="Contents")
    limit_content = fields.Text(translate=True, string="Also contents")
    exclusions = fields.Char(string="Excludes")
    # Parent hierarchy
    parent_id = fields.Many2one(comodel_name='res.partner.nace',
                                ondelete='restrict')
    children = fields.One2many(comodel_name='res.partner.nace',
                               inverse_name='parent_id')
    parent_left = fields.Integer('Parent Left', select=True)
    parent_right = fields.Integer('Parent Right', select=True)
