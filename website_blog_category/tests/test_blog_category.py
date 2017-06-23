# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestBlogCategory(TransactionCase):

    def setUp(self):
        super(TestBlogCategory, self).setUp()
        self.category_parent = self.env.ref(
            'website_blog_category.blog_category_technology',
        )
        self.category_child = self.env.ref(
            'website_blog_category.blog_category_cms',
        )

    def test_compute_post_count_parent(self):
        """ It should compute the correct number of posts as parent. """
        self.assertEqual(
            self.category_parent.post_count, 2,
        )

    def test_compute_post_count_no_child(self):
        """ It should compute the correct number of posts with no child. """
        self.assertEqual(
            self.category_child.post_count, 1,
        )

    def test_compute_all_post_ids(self):
        """ It should compute the correct posts. """
        self.assertEqual(
            self.category_child.all_post_ids,
            self.category_child.post_ids,
        )

    def test_check_parent_id_child_id(self):
        """ It should not allow disparate blog connections. """
        blog = self.env['blog.blog'].create({
            'name': 'Test Blog',
        })
        category = self.env['blog.category'].create({
            'name': 'Test category',
            'blog_id': blog.id,
        })
        with self.assertRaises(ValidationError):
            self.category_child.parent_id = category.id
