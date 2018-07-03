# -*- coding: utf-8 -*-#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.http import request
from openerp import models
import json


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def _dispatch(self):
        x = super(IrHttp, self)._dispatch()
        if request.context.get('website_version_ce_experiment'):
            data = json.dumps(
                request.context['website_version_ce_experiment'],
                ensure_ascii=False)
            x.set_cookie('website_version_ce_experiment', data)
        return x
