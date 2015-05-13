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
from openerp import api, fields, models


class WebsiteConfigSettings(models.TransientModel):

    """Settings for the OSC."""

    _inherit = 'website.config.settings'

    group_website_sale_terms_conditions = fields.Boolean(
        string="Terms and Conditions",
        implied_group='website_sale_osc.group_website_sale_terms_conditions',
        help="Enable Terms and Conditions on the Checkout")
    use_osc = fields.Boolean(
        related='website_id.use_osc',
        string='Use OSC')
    use_all_checkout_countries = fields.Boolean(
        related='website_id.use_all_checkout_countries',
        string='Use All Countries in Checkout')
    checkout_country_ids = fields.Many2many(
        related='website_id.checkout_country_ids',
        relation='res.country',
        string='Checkout Countries')

    @api.multi
    def write(self, vals):
        """
        Add or remove website settings.

        Default Checkout, One Step Checkout and Terms and Conditions
        for portal and public users.
        """
        setting = []
        group_checkout_terms = self.env['ir.model.data'].xmlid_to_res_id(
            'website_sale_osc.group_website_sale_terms_conditions')
        if 'group_website_sale_terms_conditions' in vals:
            if vals['group_website_sale_terms_conditions']:
                setting.append((4, group_checkout_terms))
            else:
                setting.append((3, group_checkout_terms))

        portal_group = self.env['ir.model.data'].xmlid_to_res_id('base.group_portal')
        users = self.env['res.users'].search([('groups_id', '=', portal_group)])

        if users:
            users.write({'groups_id': setting})

        public_user = self.env.ref('base.public_user')

        if public_user:
            public_user.write({'groups_id': setting})

        return super(WebsiteConfigSettings, self).write(vals)


class SaleConfiguration(models.TransientModel):

    """Settings for the OSC."""

    _inherit = 'sale.config.settings'

    @api.multi
    def write(self, vals):
        """
        Add or remove sale settings.

        Different shipping address for portal and public users.
        """
        setting = []
        group_shipping = self.env['ir.model.data'].xmlid_to_res_id(
            'sale.group_delivery_invoice_address')
        if 'group_sale_delivery_address' in vals:
            if vals['group_sale_delivery_address']:
                setting.append((4, group_shipping))
            else:
                setting.append((3, group_shipping))

        portal_group = self.env['ir.model.data'].xmlid_to_res_id('base.group_portal')
        users = self.env['res.users'].search([('groups_id', '=', portal_group)])

        if users:
            users.write({'groups_id': setting})

        public_user = self.env.ref('base.public_user')

        if public_user:
            public_user.write({'groups_id': setting})

        return super(SaleConfiguration, self).write(vals)
