# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
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


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    @api.one
    @api.onchange('better_zip_id')
    def on_change_city(self):
        if self.better_zip_id:
            self.zip = self.better_zip_id.name
            self.city = self.better_zip_id.city
            self.state_id = self.better_zip_id.state_id
            self.country_id = self.better_zip_id.country_id

    better_zip_id = fields.Many2one(
        'res.better.zip',
        string='Location',
        select=1,
        help='Use the city name or the zip code to search the location',
    )
