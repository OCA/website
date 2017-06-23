# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BlogCategory(models.Model):

    _name = 'blog.category'
    _inherit = ['website.seo.metadata']
    _description = 'Blog Category'
    _order = 'name'

    name = fields.Char(
        required=True,
        help='Canonical',
    )
    blog_id = fields.Many2one(
        string='Blog',
        comodel_name='blog.blog',
        required=True,
    )
    parent_id = fields.Many2one(
        string='Parent',
        comodel_name='blog.category',
        domain="[('blog_id', '=', blog_id)]",
    )
    child_ids = fields.One2many(
        string='Children',
        comodel_name='blog.category',
        inverse_name='parent_id',
    )
    post_ids = fields.One2many(
        string='Posts',
        comodel_name='blog.post',
        inverse_name='website_category_id',
    )
    all_post_ids = fields.Many2many(
        string='All Posts',
        comodel_name='blog.post',
        compute='_compute_all_post_ids',
        readonly=True,
    )
    post_count = fields.Integer(
        string='Post Count',
        compute='_compute_post_count',
        readonly=True,
    )

    _sql_constraints = [
        ('blog_id_name_uniq', 'UNIQUE(blog_id, name)',
         'Category name already exists in this blog.'),
    ]

    @api.multi
    @api.depends('post_ids', 'child_ids')
    def _compute_all_post_ids(self):
        for record in self:
            posts = self.env['blog.post'].search([
                ('website_category_id', 'child_of', [record.id]),
            ])
            record.all_post_ids = [(6, 0, posts.ids)]

    @api.multi
    @api.depends('all_post_ids')
    def _compute_post_count(self):
        for record in self:
            record.post_count = len(record.all_post_ids)

    @api.multi
    @api.constrains('parent_id', 'child_ids')
    def _check_parent_id_child_id(self):
        """ No relationship between disparate blogs. """
        for record in self:
            matches = record.child_ids.filtered(
                lambda s: s.blog_id != s.parent_id.blog_id
            )
            conditions = (len(matches),
                          record.blog_id != record.parent_id.blog_id)
            if any(conditions):
                raise ValidationError(_(
                    'Cannot assign a parent/child relationship between '
                    'categories in disparate blogs.',
                ))
