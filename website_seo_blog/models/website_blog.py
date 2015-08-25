# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, an open source suite of business apps
# This module copyright (C) 2015 bloopark systems (<http://bloopark.de>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import api, fields, models
from openerp.addons.website_seo.models.website import slug
from openerp.tools.translate import _


class Blog(models.Model):

    """Add SEO url handling for blogs."""

    _inherit = 'blog.blog'

    name = fields.Char(translate=True)
    seo_url = fields.Char(
        help='If you create or update a blog and this field is empty it is '
        'filled automatically when you enter a blog name.\nIf you fill out '
        'this field manually the allowed characters are a-z, A-Z, 0-9, - and '
        '_.\nAfter changing the SEO url you also have to update the blog menu '
        'entry in Settings -> Configuration -> Website Settings -> Configure '
        'website menus (also take care of the blog SEO url and blog menu entry'
        ' translations).\nImportant: If you use the SEO url as link, e. g. in '
        'the blog menu entry, you have to add "blog-" at the beginning. It '
        'is needed to identify the blog correctly. Example: If your SEO url is'
        ' "our-news" the link is "blog-our-news".')

    _sql_constraints = [
        ('seo_url_uniq', 'unique(seo_url)', _('SEO url must be unique!'))
    ]

    @api.multi
    def onchange_name(self, name=False, seo_url=False):
        """If SEO url is empty generate the SEO url when changing the name."""
        if name and not seo_url:
            return {'value': {'seo_url': slug((1, name))}}

        return {}

    @api.model
    def add_seo_url(self):
        """Add SEO urls for existing blogs and blog posts.

        If this module will be installed this function is called. It is needed
        for existing databases with existing blogs and blog posts.
        """
        for blog in self.env['blog.blog'].search([('seo_url', '=', False)]):
            blog.write({'seo_url': slug(blog)})
        for post in self.env['blog.post'].search([('seo_url', '=', False)]):
            post.write({'seo_url': slug(post)})

        return True


class BlogPost(models.Model):

    """Add SEO url handling for blog posts."""

    _inherit = 'blog.post'

    seo_url = fields.Char(
        help='If you create or update a blog post and this field is empty it '
        'is filled automatically when you enter a blog post name.\nIf you fill'
        ' out this field manually the allowed characters are a-z, A-Z, 0-9, - '
        'and _.')

    _sql_constraints = [
        ('seo_url_uniq', 'unique(seo_url)', _('SEO url must be unique!'))
    ]

    @api.model
    def create(self, vals):
        """Add check for correct SEO urls.

        Normally this case happens when a blog post is created in the frontend.
        """
        if vals.get('name', False) and not vals.get('seo_url', False):
            vals['seo_url'] = slug((1, vals['name']))

        return super(BlogPost, self).create(vals)

    @api.multi
    def onchange_name(self, name=False, seo_url=False):
        """If SEO url is empty generate the SEO url when changing the name."""
        return self.env['blog.blog'].onchange_name(name, seo_url)
