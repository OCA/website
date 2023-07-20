# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import ormcache
from ..tools.image import base64_to_image


class IrQweb(models.AbstractModel):
    _inherit = "ir.qweb"

    def _post_processing_att(self, tagName, atts, options):
        atts = super(IrQweb, self)._post_processing_att(tagName, atts, options)

        width = options.get("explicit_image_width")
        height = options.get("explicit_image_height")
        if width and height:
            atts["width"] = width
            atts["height"] = height
        return atts


class Image(models.AbstractModel):
    _inherit = "ir.qweb.field.image"

    @ormcache("base64_signature")
    @api.model
    def _get_image_size(self, record, field_name, base64_signature):
        base64_source = record[field_name]
        image = base64_to_image(base64_source)
        width, height = image.size
        return width, height

    @api.model
    def record_to_html(self, record, field_name, options):
        base64_signature = False
        if record and hasattr(record, field_name) and record[field_name]:
            base64_signature = record[field_name][:256]
        # don't process empty source or SVG
        if not base64_signature or base64_signature[:1] in (b"P", "P"):
            return super(Image, self).record_to_html(record, field_name, options)

        width, height = self._get_image_size(record, field_name, base64_signature)

        template_options = options.get("template_options", {}).copy()
        template_options["explicit_image_width"] = width
        template_options["explicit_image_height"] = height
        options["template_options"] = template_options

        return super(Image, self).record_to_html(record, field_name, options)
