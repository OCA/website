# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class BlogCategory(models.Model):
    _name = 'blog.category'

    name = fields.Char(String='name', help="Name of this category")
    post_ids = fields.Many2many('blog.post', string='Posts')
