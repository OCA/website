# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class blog_category(models.Model):
    _name = 'blog.category'
    _description = ''

    name = fields.Char(String='name', help="Name of this category")

    post_ids = fields.Many2many('blog.post', string='Posts')

