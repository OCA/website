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

    display_type = fields.Selection(
        string="Display Type",
        selection="_get_display_types",
        required=True,
        default='no_teaser')

    @api.one
    def set_all_posts(self):
        posts = self.env['blog.post'].search([(
            'blog_id', '=', self.id)])
        posts.write({'display_type': self.display_type})
        return {}
