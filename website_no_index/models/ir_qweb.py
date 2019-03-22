# -*- coding: utf-8 -*-
from odoo import models, api
from ..tools import noindex


class IrQWeb(models.AbstractModel):
    _inherit = 'ir.qweb'

    @api.model
    def render(self, id_or_xml_id, values=None, **options):
        """
        Makes available the functions of the package noindex to all templates.
        """
        vals = {
            'noindex': noindex,
        }
        vals.update(values or {})
        return super(IrQWeb, self).render(id_or_xml_id, values=vals, **options)
