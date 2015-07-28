# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Agile Business Group (<http://www.agilebg.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'
    country_line_ids = fields.One2many(
        'ir.ui.view.country.line', 'main_view_id', 'Localized views')
    main_view_line_ids = fields.One2many(
        'ir.ui.view.country.line', 'localized_view_id', 'Main views',
        readonly=True)


class IrUiViewCountryLine(models.Model):
    _name = 'ir.ui.view.country.line'
    _rec_name = 'main_view_id'
    main_view_id = fields.Many2one('ir.ui.view', 'Main View', required=True)
    country_id = fields.Many2one('res.country', 'Country', required=True)
    localized_view_id = fields.Many2one(
        'ir.ui.view', 'Localized View', required=True)
