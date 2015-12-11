# -*- coding: utf-8 -*-
#
#    © 2015 Agile Business Group (<http://www.agilebg.com>)
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#    See __openerp__.py file
#

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
