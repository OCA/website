# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models
from openerp.tools import mail

old_allowed_tags = mail.allowed_tags
mail.allowed_tags = old_allowed_tags | frozenset(['t'])


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    def is_node_branded(self, node):
        if(node.attrib.get('t-ignore-branding')):
            return False
        return super(
            IrUiView, self).is_node_branded(node=node)
