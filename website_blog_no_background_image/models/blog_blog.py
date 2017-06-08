# -*- coding: utf-8 -*-
# © 2015 Therp B.V, Giovanni Francesco Capalbo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class WebsiteBlog(models.Model):

    _inherit = 'blog.blog'

    def _get_image_options(self):
        return [('no_image', "No header image"),
                ('small_image', "Show small header image"),
                ('big_image', "Show big header image")
                ]

    background_image_show = fields.Selection(
        string="Default blog-wide setting for background image",
        selection=lambda self: self._get_image_options(),
        default='no_image',
        required=True,
        help="allows to set default header image formatting "
             "of the posts of this blog, the setting "
             "can be changed per blog entry later.")
