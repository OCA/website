# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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

import logging
_logger = logging.getLogger(__name__)
from openerp import models, api
from openerp.addons.website.models import website


class product_template_redirection_to_front_office(models.Model):
    """ Adds an action to go to the shop to product template."""
    _inherit = 'product.template'

    @api.model
    def action_redirection_to_front_office(self, product_template_id):
        _logger.debug('action_redirection_to_front_office')
        # The id is sometime returned as an list of single id.
        if isinstance(product_template_id, list):
            product_template_id = product_template_id[0]

        product_template = self.browse(product_template_id)
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/shop/product/%s' % website.slug(product_template)
        }
