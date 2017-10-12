# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
import logging
from lxml import html
from openerp.tests.common import HttpCase

_logger = logging.getLogger(__name__)


class HTMLCase(HttpCase):
    def setUp(self):
        super(HTMLCase, self).setUp()
        with self.cursor() as cr:
            env = self.env(cr)
            self.blog_id = env["blog.blog"].create({
                "name": "Test blog",
            }).id
            Post = env["blog.post"]
            # Create a post with cover image but no image in content
            Post.create({
                "name": "Post 1",
                "content": "A covered post",
                "cover_properties":
                    json.dumps({"background-image": "url(/post-1)"}),
                "website_published": True,
                "blog_id": self.blog_id
            })
            # Create a post like the previous one, but url is double-quoted
            Post.create({
                "name": "Post 2",
                "content": "A covered post",
                "cover_properties":
                    json.dumps({"background-image": 'url("/post-2")'}),
                "website_published": True,
                "blog_id": self.blog_id
            })
            # Create a post like the previous one, but url is single-quoted
            Post.create({
                "name": "Post 3",
                "content": "A covered post",
                "cover_properties":
                    json.dumps({"background-image": "url('/post-3')"}),
                "website_published": True,
                "blog_id": self.blog_id
            })
            # Create a post with malformed cover_properties and no cover, but
            # with background image in content
            Post.create({
                "name": "Post 4",
                "content":
                    "<div style='background-image:url(/post-4)'>Badly</div>",
                "cover_properties": "malformed",
                "website_published": True,
                "blog_id": self.blog_id
            })
            # Create a post with default cover_properties and <img> in content
            Post.create({
                "name": "Post 5",
                "content": "Cool post with image <img src='/post-5'/>",
                "website_published": True,
                "blog_id": self.blog_id
            })
            # Create a post with no images
            Post.create({
                "name": "Post 6",
                "content": "Really boring",
                "website_published": True,
                "blog_id": self.blog_id
            })
            # Create a post with lots of words
            Post.create({
                "name": "Post 7",
                "content": "Lots of words " * 80,
                "website_published": True,
                "blog_id": self.blog_id
            })

        # Open the blog index and store its HTML content
        self.html = html.document_fromstring(
            self.url_open(
                "/blog/test-blog-%d" % self.blog_id,
                timeout=30).read())

    def container(self, post_title):
        """Find the container of a blog post with given title."""
        query = u"""
            .//div[@id='main_column']/div
            [.//h2[contains(text(), "{}")]]
        """
        return self.html.xpath(query.format(post_title))[0]

    def image(self, container):
        """Find the extracted image URL in a given container."""
        query = ".//div[contains(@class, 'excerpt-img')]/img"
        return container.xpath(query)[0].attrib["src"]

    def text(self, container):
        """Find the text excerpt in a given container."""
        query = ".//div[contains(@class, 'excerpt-txt')]/p[1]"
        return container.xpath(query)[0].text_content().strip()

    def test_cover_bg_unquoted(self):
        """Cover image without quotes."""
        container = self.container("Post 1")
        self.assertEqual(self.text(container), "A covered post")
        self.assertEqual(self.image(container), "/post-1")

    def test_cover_bg_double_quoted(self):
        """Cover image with double quotes."""
        container = self.container("Post 2")
        self.assertEqual(self.text(container), "A covered post")
        self.assertEqual(self.image(container), "/post-2")

    def test_cover_bg_single_quoted(self):
        """Cover image with single quotes."""
        container = self.container("Post 3")
        self.assertEqual(self.text(container), "A covered post")
        self.assertEqual(self.image(container), "/post-3")

    def test_cover_malformed(self):
        """Cover image malformed properties and background in content."""
        container = self.container("Post 4")
        self.assertEqual(self.text(container), "Badly")
        self.assertEqual(self.image(container), "/post-4")

    def test_content_img(self):
        """No cover image, <img> element in content."""
        container = self.container("Post 5")
        self.assertEqual(self.text(container), "Cool post with image")
        self.assertEqual(self.image(container), "/post-5")

    def test_no_img(self):
        """No image anywhere."""
        container = self.container("Post 6")
        self.assertEqual(self.text(container), "Really boring")
        with self.assertRaises(IndexError):
            self.image(container)

    def test_text_excerpt(self):
        """Lots of words get truncated."""
        container = self.container("Post 7")
        text = self.text(container)
        self.assertEqual(len(text.split()), 80)
