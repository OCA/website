# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from openerp import models


class BlogPost(models.Model):
    _inherit = "blog.post"

    def main_image(self):
        """Get blog's main image URL."""
        Converter = self.env['ir.fields.converter']
        html = self.content
        # Get a dictionary of properties, avoiding possible malformed ones
        try:
            properties = json.loads(self.cover_properties)
        except (TypeError, ValueError):
            properties = dict()
        # Prepend cover image to post content, if there is one
        cover = properties.pop("background-image", "none")
        if cover and cover != "none":
            html = u"<div style={q}background-image:{}{q}/>{}".format(
                cover,
                html,
                q='"' if '"' not in cover else "'",
            )
        # Return the first found image URL or None
        try:
            return next(Converter.imgs_from_html(html, 1))
        except StopIteration:
            return None

    def content_excerpt(self, length=80):
        """Get the blog post content excerpt."""
        return self.env['ir.fields.converter'].text_from_html(
            self.content,
            length,
        )
