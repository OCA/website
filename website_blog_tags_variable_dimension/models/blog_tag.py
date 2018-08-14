# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
import random

class BlogTag(models.Model):
    _inherit = 'blog.tag'

    # doing it for all blogs. need to make it per-blog.
    min_font = 10.0
    max_font = 19.0

    @api.multi
    def get_blog_most_used_tag_cardinality(self):
        tags = self.env['blog.tag'].search([])
        # NOTE no need to iterate recordset, same value for all records.
        """
        NOTE setting max ranking to 1 to avoid division by 0 when there are 
        no blogposts with tags.
        """
        max_ranking = 1
        for tag in tags:
            max_ranking = max(
                len(tag.post_ids), 
                max_ranking
            )
        for this in self:
            this.max_ranking = float(max_ranking)
        
    max_ranking = fields.Float( 
        string="Higest tag cardinality in this blog", 
        compute=get_blog_most_used_tag_cardinality,
        required=True,
        help="The number of times the most used tag is used in this blog"
    )
 
    @api.multi
    def get_font_size(self):
        for this in self:
            hits = len(this.post_ids.ids)
            this.font_size_in_cloud = int(
                (hits)/(this.max_ranking) * (
                    this.max_font - this.min_font
                ) + this.min_font
            )

    @api.multi
    def get_tag_cardinality(self):
        for this in self:
            this.tag_cardinality = len(this.post_ids.ids)

    @api.multi
    def compute_color(self):
        for this in self:
            # green therp, darkgreen, blue, orange
            # hastable allows me to use better performing randint here too.
            # TODO EXTEND THE THREE COLORS , TO BE SELECTE<F5><F6>D
            hashtable = {1:'#7b7655', 2: '#006400', 3: '#4682B4', 4: '#ffa500'}
            this.random_color = hashtable[random.randint(1,4)]

    tag_cardinality = fields.Integer(
            string="In how many posts is the tag used", 
            compute=get_tag_cardinality,
            required=True,
        )

    font_size_in_cloud = fields.Integer(
        string="Font Size of tag in cloud",
        help="size of tag font from 8 to 24 px relative"
             "to the most used tag, that will be allways displayed at 24px",
        compute=get_font_size,
        required=True,
    )
    
    random_color = fields.Char(
        string="random color of tag in cloud",
        compute=compute_color, 
    )

    def randomize_recordset(self):
        return random.sample(self, len(self))

