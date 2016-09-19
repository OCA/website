# -*- coding: utf-8 -*-
from openerp.http import request, STATIC_CACHE
from openerp.addons.web import http
from openerp import _
import logging
logger = logging.getLogger(__name__)


class Web_Editor(http.Controller):

    #------------------------------------------------------
    # remove images
    #------------------------------------------------------
    @http.route('/website/image/remove', type='json', auth='user')
    def remove(self, image_id):
        """
        @param image_id: base_multi_image.image image id
        @return: empty dict if all ok else dict with key error
        """
        BaseImage = request.env['base_multi_image.image']
        image = BaseImage.browse(image_id)
        result = {}
        try:
            image.unlink()
        except Exception, e:
            logger.exception(_("Failed to remove image"))
            message = unicode(e)
            result.update({'error': message})
        return result

    # ------------------------------------------------------
    # Make main image
    # ------------------------------------------------------
    @http.route('/website/image/main', type='json', auth='user')
    def make_main_image(self, image_id):
        """
        @param image_id: base_multi_image.image image id
        @return: empty dict if all ok else dict with key error
        """

        BaseImage = request.env['base_multi_image.image']
        image = BaseImage.browse(image_id)
        image.sequence = 10

        secondary_images = BaseImage.search([
            ('owner_model', '=', image.owner_model),
            ('owner_id', '=', image.owner_id),
            ('id', '!=', image_id),
        ])
        result = {}
        try:
            secondary_images.write({'sequence': 20})
        except Exception, e:
            logger.exception(_("Failed to set main image"))
            message = unicode(e)
            result.update({'error': message})
        return result
