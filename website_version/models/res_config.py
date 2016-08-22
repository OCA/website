# -*- coding: utf-8 -*-
##############################################################################
#
# Authors: Odoo S.A., Nicolas Petit (Clouder)
# Copyright 2016, TODAY Odoo S.A. Clouder SASU
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, models, api


class AnalyticsConfigSettings(models.TransientModel):

    _inherit = 'base.config.settings'
    
    ga_sync = fields.Boolean("Show tutorial to know how to get my 'Client ID' and my 'Client Secret'")
    ga_client_id = fields.Char('Client ID')
    ga_client_secret = fields.Char('Client Secret')
    google_management_authorization = fields.Char('Google authorization')
    
    @api.model
    def set_analytics(self, ids):
        params = self.env['ir.config_parameter']
        myself = self.browse(ids[0])
        params.set_param('google_management_client_id', myself.ga_client_id or '', groups=['base.group_system'])
        params.set_param('google_management_client_secret', myself.ga_client_secret or '', groups=['base.group_system'])
        
    @api.model
    def get_analytics(self, ids):
        params = self.env.get('ir.config_parameter')
        ga_client_id = params.get_param('google_management_client_id', default='')
        ga_client_secret = params.get_param('google_management_client_secret', default='')
        return dict(ga_client_id=ga_client_id, ga_client_secret=ga_client_secret)
