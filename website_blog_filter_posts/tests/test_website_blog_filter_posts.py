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
from openerp.addons.website_blog.tests.common import TestWebsiteBlogCommon


class TestWebsiteBlogFilterPosts(TestWebsiteBlogCommon):

    def setUp(self):
        super(TestWebsiteBlogFilterPosts, self).setUp()
        self.blog_blog_obj = self.env['blog.blog']
        self.blog_post_obj = self.env['blog.post']
        # create a new blog
        self.test_blog = self.blog_blog_obj.sudo(self.user_blogmanager.create({
            'name': 'New Test Blog',
            'description': 'This is a test blog.'
        }))

        self.test_blog_post_1 = self.blog_post_obj.sudo(selg.user_blogmanager.create({
            'name': 'Blog Post 1',
            'blog_id': self.test_blog.id
        }))
