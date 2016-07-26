# -*- coding: utf-8 -*-
# (C) 2015 Therp BV <http://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    def is_node_branded(self, node):
        if(node.attrib.get('t-ignore-branding')):
            return False
        return super(
            IrUiView, self).is_node_branded(node=node)
