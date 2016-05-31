# -*- coding: utf-8 -*-
# © 2015-2016 Odoo S.A.
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def get_access_action(self):
        """Override method that generated the link to access the document.

        Instead of the classic form view, redirect to the online quote if
        exists.
        """
        self.ensure_one()
        if self.state in ['draft', 'cancel']:
            return super(sale_order, self).get_access_action()
        return {
            'type': 'ir.actions.act_url',
            'url': '/my/orders/%s' % self.id,
            'target': 'self',
            'res_id': self.id,
        }
