# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import io
import base64
import json

from odoo import http
from odoo.http import request
from PIL import Image


class MainController(http.Controller):
    @http.route('/website_adv_image_optimization/attachment/optimize',
                type='http', auth='user', methods=['POST'])
    def optimize(self, attachment_id, quality=80,
                 width=False, height=False, **kwargs):
        # Not using odoo.tools.image so I can reuse variables
        attachment_obj = request.env['ir.attachment']
        attachment = attachment_obj.search([('id', '=', attachment_id)])
        image = Image.open(io.BytesIO(base64.b64decode(attachment.datas)))

        # Only resize when needed
        width = int(width)
        height = int(height)
        if width and height and \
           width > 0 and height > 0 and \
           (width != image.size[0] or height != image.size[1]):
            self._resize(image, width, height)

        buffer = io.BytesIO()
        self._update_quality(image, quality, buffer)
        image.close()
        data = buffer.getvalue()

        # Not nice but needed to let GUI refresh
        if '_adv_opt' not in attachment.name:
            new_name = attachment.name + '_adv_opt(1)'
        else:
            count = str(int(attachment.name[-2:-1]) + 1)
            new_name = attachment.name[0:-2] + count + ')'

        attachment.write({
            'datas': base64.b64encode(data),
            'name': new_name
        })
        return json.dumps(True)

    def _resize(self, image, width, height):
        image.thumbnail((width, height), Image.ANTIALIAS)

    def _update_quality(self, image, quality, buffer):
        opt = dict(format=image.format)
        opt.update(optimize=True, quality=int(quality))
        image.save(buffer, **opt)
