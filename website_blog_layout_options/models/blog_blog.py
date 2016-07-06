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
from openerp import models, fields, api


class WebsiteBlog(models.Model):

    _inherit = 'blog.blog'

    @api.model
    def _get_display_types(self):
        return [('no_teaser', 'Show Title with no teaser'),
                ('teaser', 'Show Title with 3 teaser lines'),
                ('complete', 'Show Title and complete blog entry')]

    def _get_image_options(self):
        return [('no_image', "No header image"),
                ('small_image', "Show small header image"),
                ('big_image', "Show big header image")
                ]

    display_type = fields.Selection(
        string="Display Type",
        selection="_get_display_types",
        required=True,
        default='no_teaser')

    thumbnail_width = fields.Selection(selection=[
        ('64', 'Small'),  ('128', 'Medium'), 
        ('256', 'Big'), ('384', 'Gigantic')],
        string="Thumbnail Size",
        help="Allows to choose thumbnail size in blog teaser and also" 
             "in content \n will be used in all blogposts of this blog",
        default='128')

    background_image_show = fields.Selection(
        string="Default blog-wide setting for background image",
        selection=lambda self: self._get_image_options(),
        default='no_image',
        required=True,
        help="allows to set default header image formatting "
             "of the posts of this blog, the setting "
             "can be changed per blog entry later.")

    @api.one
    def set_all_posts(self):
        posts = self.env['blog.post'].search([(
            'blog_id', '=', self.id)])
        posts.write({'display_type': self.display_type})
        return {}



