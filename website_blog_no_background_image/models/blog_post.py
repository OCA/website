# -*- coding: utf-8 -*-
# © 2015 Therp B.V, Giovanni Francesco Capalbo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class BlogPost(models.Model):

    _inherit = 'blog.post'

    background_image_show = fields.Selection(
        string="Type of header image on blog post",
        selection=lambda self: self.blog_id._get_image_options(),
        default=lambda self: self.blog_id.background_image_show,
        required=True,
        help="Choose if how you want to display the blog post:"
        "Just the title above the post, a small header image"
        "above the blog post title, or a big full screen image,"
        "before showing the post, (odoo default)")

    @api.onchange('blog_id')
    def set_new_default(self):
        self.background_image_show = self.blog_id.background_image_show
