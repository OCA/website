# Copyright 2018 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.addons.portal.controllers.mail import PortalChatter


class PortalChatterWithAttachments(PortalChatter):

    @http.route(['/mail/chatter_post'], type='http', methods=['POST'],
                auth='public', website=True)
    def portal_chatter_post(self, res_model, res_id, message, **kw):
        attachment = kw.pop('attachment', None)
        if attachment:
            attachments = [(attachment.filename, attachment.read())]
            kw['attachments'] = attachments

        return super().portal_chatter_post(
            res_model, res_id, message, **kw)
