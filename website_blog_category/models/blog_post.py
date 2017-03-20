# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


import logging
_logger = logging.getLogger(__name__)


class BlogPost(models.Model):

    _inherit = 'blog.post'

    website_category_id = fields.Many2one(
        string='Website Category',
        comodel_name='blog.category',
    )

    @api.model
    def search(self, domain, *args, **kwargs):
        if self.env.context.get('search_category_id'):
            category = self.env.context['search_category_id']
            domain += [
                ('website_category_id', 'child_of', category),
            ]
        _logger.debug(domain)
        return super(BlogPost, self).search(domain, *args, **kwargs)
