# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models
from openerp.http import request


class IrHttp(models.Model):
    _inherit = 'ir.http'

    def _dispatch(self):
        """Force backend language on frontend"""
        response = super(IrHttp, self)._dispatch()
        if not request.website_enabled and hasattr(response, 'set_cookie') and\
           request.httprequest.cookies.get('website_lang') != request.lang:
            response.set_cookie('website_lang', request.lang)
        return response
