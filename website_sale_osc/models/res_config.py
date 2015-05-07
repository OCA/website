# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, an open source suite of business apps
# This module copyright (C) 2015 bloopark systems (<http://bloopark.de>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv


class website_config_settings(osv.osv_memory):
    _inherit = 'website.config.settings'

    _columns = {
        'group_website_sale_terms_conditions': fields.boolean(
            "Terms and Conditions",
            implied_group='website_sale_osc.group_website_sale_terms_conditions',
            help="Enable Terms and Conditions on the Checkout"),
        'use_osc': fields.related('website_id', 'use_osc', type='boolean', string='Use OSC'),
        'use_all_checkout_countries': fields.related('website_id', 'use_all_checkout_countries',
                                                     type='boolean',
                                                     string='Use All Countries in Checkout'),
        'checkout_country_ids': fields.related('website_id', 'checkout_country_ids',
                                               type='many2many', relation='res.country',
                                               string='Checkout Countries'),
    }

    def write(self, cr, uid, ids, vals, context=None):
        """
        Add or remove website settings (Default Checkout, One Step Checkout and
        Terms and Conditions) for portal and public users.
        """
        setting = []
        group_checkout_terms = self.pool.get('ir.model.data').get_object_reference(
            cr, uid, 'website_sale_osc', 'group_website_sale_terms_conditions')
        if 'group_website_sale_terms_conditions' in vals:
            if vals['group_website_sale_terms_conditions']:
                setting.append((4, group_checkout_terms[1]))
            else:
                setting.append((3, group_checkout_terms[1]))

        portal_group = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'base',
                                                                           'group_portal')
        user_ids = self.pool.get('res.users').search(cr, uid, [('groups_id', '=', portal_group[1])])

        public_user = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'base',
                                                                          'public_user')
        user_ids.append(public_user[1])

        if user_ids:
            self.pool.get('res.users').write(cr, uid, user_ids, {'groups_id': setting})

        return super(website_config_settings, self).write(cr, uid, ids, vals, context)
