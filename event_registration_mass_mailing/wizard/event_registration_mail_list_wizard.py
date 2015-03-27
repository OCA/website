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

from openerp import models, api, fields


class EventRegistrationMailListWizard(models.TransientModel):
    _name = "event.registration.mail.list.wizard"
    _description = "Create contact mailing list"

    mail_list = fields.Many2one(comodel_name="mail.mass_mailing.list",
                                string="Mailing list")
    event_registrations = fields.Many2many(comodel_name="event.registration",
                                           relation="mail_list_wizard_event"
                                           "_registration")

    @api.multi
    def add_to_mail_list(self):
        contact_obj = self.env['mail.mass_mailing.contact']
        registration_obj = self.env['event.registration']
        for registration_id in self.env.context.get('active_ids', []):
            registration = registration_obj.browse(registration_id)
            criteria = [('email', '=', registration.email),
                        ('list_id', '=', self.mail_list.id)]
            contact_test = contact_obj.search(criteria)
            if contact_test:
                continue
            contact_vals = {
                'email': registration.email,
                'name': registration.name,
                'list_id': self.mail_list.id
            }
            contact_obj.create(contact_vals)
