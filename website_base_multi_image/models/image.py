# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

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
        for key, image in post.iteritems():
            if key.startswith('new_image_'):
                if isinstance(image, list):
                    new_image = image[0]
                else:
                    new_image = image
                images_to_add.append((0, 0, {
                    'storage': 'db',
                    'file_db_store': base64.encodestring(new_image.read()),
                    'owner_model': model_name,
                    'name': new_image.filename,
                    'extension': 'jpg',
                }))
        return images_to_add
