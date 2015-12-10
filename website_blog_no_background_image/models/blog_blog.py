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
