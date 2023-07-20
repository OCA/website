# -*- coding: utf-8 -*-
import base64
import binascii
import io

from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.tools import Image


def base64_to_image(base64_source):
    """Return a PIL image from the given `base64_source`.

    :param base64_source: the image base64 encoded
    :type base64_source: string or bytes

    :return: the PIL image
    :rtype: PIL.Image

    :raise: UserError if the base64 is incorrect or the image can't be identified by PIL
    """
    try:
        return Image.open(io.BytesIO(base64.b64decode(base64_source)))
    except (OSError, binascii.Error):
        raise UserError(_("This file could not be decoded as an image file."
                          "Please try with a different file."))
