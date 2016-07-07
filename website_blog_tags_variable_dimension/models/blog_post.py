# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class BlogTag(models.Model):
    _inherit = 'blog.tag'

    # doing it for all blogs. need to make it per-blog.
    min_font=8
    max_font=24

    @api.multi
    def get_blog_most_used_tag_cardinality(self):
        posts =  self.env['blog.post'].search([])
        tags = self.env['blog.tag'].search([])
        max_ranking = 0
        for tag in tags:
            max_ranking = max(
                len(posts.filtered(lambda x: tag.id in x.tag_ids)), 
                    tag.max_ranking
            )
        return max_ranking
    
    max_ranking = fields.Integer( 
        string="Higest tag cardinality in this blog", 
        compute=get_blog_most_used_tag_cardinality,
        help="The number of times the most used tag is used in this blog"
    )


    @api.multi
    def get_font_size(self):
        posts =  self.env['blog.post'].search([])
        hits = len(posts.filtered(lambda x: self.id in x.tag_ids))
        return int(
            (hits)/(self.max_ranking) * (
                self.max_font - self.min_font
            ) + self.min_font
        )


    font_size_in_cloud = fields.Integer(
        string="Font Size of tag in cloud",
        help="size of tag font from 8 to 24 px relative"
             "to the most used tag, that will be allways displayed at 24px",
        compute=get_font_size
    )

