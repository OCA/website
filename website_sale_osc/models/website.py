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
from openerp.osv import osv, fields


class website(osv.osv):
    _inherit = 'website'

    _columns = {
        'use_osc': fields.boolean('Use OSC'),
        'use_all_checkout_countries': fields.boolean('Use All Countries in Checkout'),
        'checkout_country_ids': fields.many2many('res.country', 'checkout_country_rel',
                                                 'website_id', 'country_id', 'Checkout Countries'),
    }
    _defaults = {
        'use_osc': True,
        'use_all_checkout_countries': True
    }
