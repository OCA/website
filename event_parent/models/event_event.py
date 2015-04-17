# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
#                 Antonio Espinosa <antonioea@antiun.com>
#                 Javier Iniesta <javieria@antiun.com>
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
import urllib
import base64
import json
import datetime

import logging
from pprint import pformat
_logger = logging.getLogger(__name__)


class EventEvent(models.Model):
    _inherit = 'event.event'

    eym_event_id = fields.Integer(
        string='Evento ID', readonly=True)
    parent_id = fields.Many2one(
        comodel_name='event.event', string='Evento padre', readonly=False)
    sessions_event = fields.One2many(
        comodel_name='event.event', inverse_name='parent_id',
        string='Sesiones')
    date_begin = fields.Datetime(
        string='Start Date', readonly=False, required=False,
        states={'draft': [('readonly', False)]})
    date_end = fields.Datetime(
        string='End Date', readonly=False, required=False,
        states={'draft': [('readonly', False)]})
