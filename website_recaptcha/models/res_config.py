# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2014 Elico Corp. All Rights Reserved.
#    Augustin Cisterne-Kaas <augustin.cisterne-kaas@elico-corp.com>
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

from openerp.osv import fields, osv


class website_config_settings(osv.osv_memory):
    _inherit = 'website.config.settings'

    # makes it overridable for custom theme
    def _select_themes(self, cr, uid, context=None):
        """ Available concepts

        Can be inherited to add custom versions.
        """
        return [('red', 'Red'),
                ('white', 'White'),
                ('blackglass', 'Blackglass'),
                ('clean', 'Clean')]

    _columns = {
        'recaptcha_public_key': fields.related(
            'website_id', 'recaptcha_public_key', type="char",
            string='reCAPTCHA Public Key'),
        'recaptcha_private_key': fields.related(
            'website_id', 'recaptcha_private_key', type="char",
            string='reCAPTCHA Private Key'),
        'recaptcha_theme': fields.related(
            'website_id', 'recaptcha_theme', type="selection",
            selection=_select_themes, string='reCAPTCHA theme', required=True)
    }

    _defaults = {
        'recaptcha_theme': 'red'
    }
