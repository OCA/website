# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class BlogBlog(models.Model):

    _inherit = 'blog.blog'

    website_category_ids = fields.One2many(
        string='Website Categories',
        comodel_name='blog.category',
        inverse_name='blog_id',
    )
