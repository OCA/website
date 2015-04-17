# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
#                 Antonio Espinosa <antonioea@antiun.com>
#                 Javier Iniesta <javieria@antiun.com>
#                 Daniel Gómez-Zurita <danielgz@antiun.com>
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

from openerp import models, fields, api

# from pprint import pformat
# import logging
# _logger = logging.getLogger(__name__)


class EventRegistrationField(models.Model):
    _name = "event.registration.field"

    _key_options_field = ['promo_source']

    event_id = fields.Many2one(comodel_name="event.event",
                               string="Id del evento")
    field_id = fields.Many2one(comodel_name='event.registration.fields',
                               string='Campo', required=True)
    is_required = fields.Boolean(string="Es obligatorio")
    options_model = fields.Selection(
        string='Modelo de opciones',
        selection=[('crm.tracking.source', 'Ventas/Origen'),
                   ('crm.case.stage', 'Ventas/Etapa'),
                   ('crm.case.categ', 'Ventas/Etiquetas de venta')])
    options_available = fields.Char(
        string='Opciones disponibles',
        help='Escribe solamente las opciones a mostrar, separadas por comas')

    # used_keys = fields.Char(compute='compute_used_keys',
    #                         store=True, readonly=True)

    # @api.one
    # @api.depends('event_id.available_fields')
    # def compute_used_keys(self):
    #     keys = []
    #     for brother in self.event_id.available_fields:
    #         if brother != self:
    #             keys.append(brother.field_id.key)
    #     self.used_keys = ','.join(keys)

    @api.onchange('field_id')
    def onchange_extra_form_field(self):
        if self.field_id.key not in self._key_options_field:
            if self.options_model:
                self.options_model = None
            if self.options_available:
                self.options_available = None
