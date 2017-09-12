# -*- coding: utf-8 -*-#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.http import request
from odoo import models
import json


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls):
        x = super(IrHttp, cls)._dispatch()
        if request.context.get('website_version_ce_experiment'):
            data = json.dumps(
                request.context['website_version_ce_experiment'],
                ensure_ascii=False)
            x.set_cookie('website_version_ce_experiment', data)
        return x
