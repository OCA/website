# -*- coding: utf-8 -*-
##############################################################################
#
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
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
