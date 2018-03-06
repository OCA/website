# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.http import request


class IrQWeb(models.AbstractModel):
    _inherit = 'ir.qweb'

    @api.model
    def render(self, id_or_xml_id, values=None, **options):
        if request and self.env.context.get("website_id") and \
                id_or_xml_id == 'web.assets_frontend':
            if values:
                values['website'] = request.website
            else:
                values = {'website': request.website}
        return super(IrQWeb, self).render(id_or_xml_id,
                                          values=values,
                                          **options)
