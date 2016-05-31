# -*- coding: utf-8 -*-
# © 2013-2016 Odoo S.A.
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models


class Website(models.Model):
    _inherit = "website"

    @api.model
    def payment_acquirers(self):
        return list(self.env['payment.acquirer'].sudo().search(
            [('website_published', '=', True)]))
