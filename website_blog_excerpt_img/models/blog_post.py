# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class BlogPost(models.Model):
    _inherit = "blog.post"

    def _default_website_meta(self):
        """Extract default OG image from post content if none is provided."""
        result = super()._default_website_meta()
        image = result['default_opengraph']['og:image']
        if not image:
            try:
                image = next(self.env['ir.fields.converter'].imgs_from_html(
                    self.content,
                    1,
                ))
            except StopIteration:
                pass  # No image
            else:
                result['default_opengraph']['og:image'] = image
                result['default_twitter']['twitter:image'] = image
        return result
