# -*- coding: utf-8 -*-
# Copyright 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from lxml import etree
from openerp import api, fields, models, tools


class BlogPost(models.Model):

    _inherit = 'blog.post'

    @api.multi
    def extract_teaser(self):
        pass

    @api.onchange('blog_id')
    def set_new_default(self):
        self.background_image_show = self.blog_id.background_image_show

    @api.depends('thumbnail')
    def _get_thumbnail(self):
        if self.thumbnail:
            self.thumbnail_binary = self.sudo().thumbnail.datas

    def _write_thumbnail(self):
        attachment_dict = {
            'name': self.name + 'thumbnail',
            'datas': self.thumbnail_binary,
            'type': 'binary',
            'res_model': 'blog.post',
            'res_id':  self.id,
        }
        new_attachment = self.env['ir.attachment'].sudo().create(
            attachment_dict
        )
        self.thumbnail = new_attachment.id

    background_image_show = fields.Selection(
        string="Type of header image on blog post",
        selection=lambda self: self.blog_id._get_image_options(),
        default=lambda self: self.blog_id.background_image_show or 'big_image',
        help="Choose if how you want to display the blog post: "
        "Just the title above the post, a small header image "
        "above the blog post title, or a big full screen image,"
        "before showing the post, (odoo default)"
    )

    thumbnail = fields.Many2one(
        string='Blog Post Thumbnail',
        comodel_name='ir.attachment',
        help='A small image shown in teaser and content'
    )

    thumbnail_binary = fields.Binary(
        string='Blog Post Thumbnail',
        compute=_get_thumbnail,
        inverse=_write_thumbnail,
        help='A small image shown in teaser and content'
    )

    display_type = fields.Selection(
        selection=lambda self: self.blog_id._get_display_types(),
        default=lambda self: self.blog_id.display_type or 'no_teaser',
        required=True,
        help="Select no_teaser if you just want the clickable title,"
             "in the list. Select Teaser if you want to display,"
             "title+first lines of post select Complete if you prefer,"
             "the entire text  to be viewed in the blog list.")

    # overwrite v10 teaser compute
    teaser = fields.Text(string='Teaser for Blog Post', compute=False)

    category_id = fields.Many2many(
        string="Categories",
        comodel_name='blog.category',
        help='Blog post category, categories are a different type of '
             'classification, other than tags'
        )
