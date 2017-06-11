# -*- coding: utf-8 -*-
# © 2014 OpenERP SA
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.osv import osv
from openerp.addons.web.http import request


class ir_http(osv.AbstractModel):
    _inherit = 'ir.http'

    def _auth_method_public(self):
        if not request.session.uid:
            domain_name = request.httprequest.environ.get('HTTP_HOST', '').split(':')[0]
            website_id = self.pool['website']._get_current_website_id(request.cr, SUPERUSER_ID, domain_name, context=request.context)
            if website_id:
                request.uid = self.pool['website'].browse(request.cr, SUPERUSER_ID, website_id, request.context).user_id.id
            else:
                dummy, request.uid = self.pool['ir.model.data'].get_object_reference(request.cr, SUPERUSER_ID, 'base', 'public_user')
        else:
            request.uid = request.session.uid
