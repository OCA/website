# Copyright 2026 Domatix <info@domatix.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import json

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestBlogPostJsonLd(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.website = cls.env.ref("website.default_website")
        cls.blog = cls.env["blog.blog"].create(
            {"name": "Test Blog", "website_id": cls.website.id}
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test Author"})
        cls.post = cls.env["blog.post"].create(
            {
                "name": "Test Post",
                "blog_id": cls.blog.id,
                "author_id": cls.partner.id,
                "post_date": "2026-08-18 10:00:00",
            }
        )

    def test_get_article_jsonld(self):
        data = json.loads(self.post._get_article_jsonld())
        self.assertEqual(data["@type"], "BlogPosting")
        self.assertEqual(data["headline"], "Test Post")
        self.assertEqual(data["author"]["name"], "Test Author")
        self.assertEqual(data["publisher"]["name"], self.website.name)
        self.assertTrue(data["url"].startswith(self.website.get_base_url()))
        self.assertIn("/blog/", data["url"])
        self.assertEqual(data["datePublished"], self.post.post_date.isoformat())

    def test_get_article_jsonld_no_author(self):
        self.post.author_id = False
        data = json.loads(self.post._get_article_jsonld())
        self.assertEqual(data["@type"], "BlogPosting")
        self.assertNotIn("author", data)
