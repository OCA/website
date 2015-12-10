# -*- coding: utf-8 -*-
# (C) 2015 Therp BV <http://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html). 
from openerp import api, fields, models


class WebsiteBlog(models.Model):

    _inherit = 'blog.blog'

    @api.model
    def _get_display_types(self):
        return [('no_teaser', 'Show title with no teaser'),
                ('teaser', 'Show title with 3 teaser lines'),
                ('complete', 'Show title and complete blog entry')]

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
