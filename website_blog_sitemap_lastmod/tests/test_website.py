# Copyright 2026 Domatix <info@domatix.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestWebsiteBlogSitemapLastmod(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.website = cls.env.ref("website.default_website")
        cls.blog = cls.env["blog.blog"].create({"name": "Test Blog"})
        cls.post = cls.env["blog.post"].create(
            {
                "name": "Test Post",
                "blog_id": cls.blog.id,
                "is_published": True,
            }
        )

    def test_blog_post_lastmod_in_sitemap(self):
        pages = list(self.website._enumerate_pages())
        slug = self.env["ir.http"]._slug
        expected_loc = f"/blog/{slug(self.blog)}/{slug(self.post)}"
        post_pages = [p for p in pages if p.get("loc") == expected_loc]
        self.assertEqual(len(post_pages), 1, "published blog post must appear once")
        self.assertEqual(post_pages[0]["lastmod"], self.post.write_date.date())

    def test_other_pages_unchanged(self):
        pages = list(self.website._enumerate_pages())
        non_blog_pages = [p for p in pages if not p.get("loc", "").startswith("/blog/")]
        self.assertTrue(non_blog_pages)
        for page in non_blog_pages:
            self.assertIsInstance(page, dict)
            self.assertIn("loc", page)
