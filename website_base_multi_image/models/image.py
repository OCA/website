# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#        Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
from openerp import api, models


class Image(models.Model):
    _inherit = "base_multi_image.image"

    @api.model
    def get_images_to_add(self, post, model_name):
        """
        @param post: dict with images in format 'new_image_xxx'
        @param model_name: Model to store image
        @return: List of images to add
        """
        images_to_add = []
        for key in post.keys():
            if 'new_image_' in key:
                if isinstance(post[key], list):
                    new_image = post[key][0]
                else:
                    new_image = post[key]
                images_to_add.append((0, 0, {
                    'storage': 'db',
                    'file_db_store': base64.encodestring(new_image.read()),
                    'owner_model': model_name,
                    'name': new_image.filename,
                    'extension': 'jpg',
                }))
        return images_to_add
