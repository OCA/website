# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api


class WebsiteBlog(models.Model):

    _inherit = 'blog.blog'

    @api.model
    def _get_image_options(self):
        return [('small_image', 
                 'Show small header image (limited to 450px in height)'),
                ('big_image', 'Show big header image (odoo default)')]

    @api.model
    def _get_display_types(self):
        return [('no_teaser', 'Show Title with no teaser'),
                ('teaser', 'Show Title with 3 teaser lines'),
                ('complete', 'Show Title and complete blog entry')]

    display_type = fields.Selection(
        string="Display Type",
        selection="_get_display_types",
        required=True,
        default='no_teaser'
    )
    thumbnail_width = fields.Selection(selection=[
        ('64', 'Small'),  ('128', 'Medium'),
        ('192', 'Big')],
        string="Thumbnail Size",
        help="Allows to choose thumbnail size in blog teaser and also"
             "in content \n will be used in all blogposts of this blog",
        default='128')
    background_image_show = fields.Selection(
        selection="_get_image_options",
        string="Default blog-wide setting for background image",
        default='small_image',
        required=True,
        help="allows to set default header image formatting "
             "of the posts of this blog, the setting "
             "can be changed per blog entry later.")

    @api.multi
    def set_all_posts(self):
        for this in self:
            posts = self.env['blog.post'].search([(
                'blog_id', '=', this.id)])
            posts.write({'display_type': this.display_type})
