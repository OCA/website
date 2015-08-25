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
from openerp.exceptions import ValidationError
from openerp.tests import common


class TestWebsiteBlogSeo(common.TransactionCase):

    """Unit tests about website blog management with SEO urls."""

    at_install = False
    post_install = True

    def setUp(self):
        """setUp with one blog and one blog post."""
        super(TestWebsiteBlogSeo, self).setUp()

        self.blog = self.env['blog.blog']
        self.post = self.env['blog.post']

        self.blog_one = self.blog.create({
            'name': 'Main Blog',
            'seo_url': 'main-blog'
        })
        self.post_one = self.post.create({
            'name': 'My First Blog Post',
            'seo_url': 'first-blogpost',
            'blog_id': self.blog_one.id
        })

    def test_00_website_seo_blog(self):
        """Test valid and invalid blog creation."""
        self.assertTrue(self.blog.create({
            'name': 'Second Blog',
            'seo_url': 'our-blog'
        }))
        with self.assertRaises(ValidationError):
            self.blog.create({
                'name': 'Second Blog',
                'seo_url': 'our-blog-!?='
            })

    def test_01_website_seo_blog(self):
        """Test valid and invalid blog post creation."""
        self.assertTrue(self.post.create({
            'name': 'My Second Blog Post',
            'seo_url': 'second-blogpost',
            'blog_id': self.blog_one.id
        }))
        with self.assertRaises(ValidationError):
            self.post.create({
                'name': 'My Third Blog Post',
                'seo_url': 'th!rd-blogpost',
                'blog_id': self.blog_one.id
            })

    def test_02_website_seo_blog(self):
        """Test valid and invalid blog update."""
        self.assertTrue(self.blog_one.write({
            'seo_url': 'main-blogger'
        }))
        with self.assertRaises(ValidationError):
            self.blog_one.write({
                'seo_url': 'main-blo&&er'
            })

    def test_03_website_seo_blog(self):
        """Test valid and invalid blog post update."""
        self.assertTrue(self.post_one.write({
            'seo_url': 'first-blog-post'
        }))
        with self.assertRaises(ValidationError):
            self.post_one.write({
                'seo_url': 'first-blog=post'
            })

    def test_04_website_seo_blog(self):
        """Test on change name event with empty and filled SEO url."""
        result = self.post.onchange_name('Ein bißchen Mehr', False)
        self.assertEqual(result['value']['seo_url'], 'ein-bichen-mehr-1')

        result = self.post.onchange_name('Ein bißchen Mehr', 'much-more')
        self.assertEqual(result, {})
