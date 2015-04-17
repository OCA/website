# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
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
from openerp.addons.website_event_register_free_with_sale.\
    controllers.website_sale import WebsiteSale
from openerp.http import request


class WebsiteSale(WebsiteSale):

    def checkout_values(self, data=None):
        values = super(WebsiteSale, self).checkout_values(data=data)
        event = request.env['event.event'].sudo().browse(
            int(request.session['event_id']))

        extra_fields = []
        select_option = []

        if 'phone' in self.mandatory_free_registration_fields:
            self.mandatory_free_registration_fields.remove('phone')
        if 'zip' in self.mandatory_free_registration_fields:
            self.mandatory_free_registration_fields.remove('zip')
        if 'city' in self.mandatory_free_registration_fields:
            self.mandatory_free_registration_fields.remove('city')
        if 'street' in self.mandatory_free_registration_fields:
            self.mandatory_free_registration_fields.remove('street')
        if 'street2' in self.mandatory_free_registration_fields:
            self.mandatory_free_registration_fields.remove('street2')

        for field in event['available_fields']:
            extra_fields.append(field.field_id.key)
            self.optional_free_registration_fields.append(field.field_id.key)
            if field.is_required:
                self.mandatory_free_registration_fields.append(
                    field.field_id.key)
            if 'options_model' in field and field.options_model:
                model = str(field['options_model'])
                list_values = field['options_available'].split(',')
                for option in list_values:
                    model_obj = request.env[model].sudo().search(
                        [('name', '=', option)])
                    if model_obj:
                        select_option.append(option)

        values['extra_fields'] = extra_fields
        if select_option:
            values['select_option'] = select_option
        return values
