# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.addons.web import http
from openerp.addons.web.http import request


class WebsiteUploadVideo(http.Controller):
    @http.route('/website_upload_video/attach',
                type='http', auth='user', methods=['POST'], website=True)
    def attach(self, upload=None):
        attachments = request.registry['ir.attachment']
        video_data = upload.read()
        attachment_id = attachments.create(request.cr, request.uid, {
            'name': upload.filename,
            'datas': video_data.encode('base64'),
            'datas_fname': upload.filename,
            'res_model': 'ir.ui.view',
        }, request.context)
        return """<script type='text/javascript'>
            window.parent['video_upload_callback'](%s);
        </script>""" % (attachment_id)
