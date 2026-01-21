# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestBlogPostUsability(TransactionCase):
    def setUp(self):
        super().setUp()
        # Create a blog
        self.blog = self.env["blog.blog"].create({"name": "Test Blog"})
        # Create a user with blog manager rights
        group_blog_manager = self.env.ref("website.group_website_designer")
        self.user_blogmanager = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": "Blog Manager",
                    "login": "blog_manager",
                    "email": "blog.manager@example.com",
                    "groups_id": [(6, 0, [group_blog_manager.id])],
                }
            )
        )
        # Create a test blog post
        self.blog_post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Test Blog Post",
                    "blog_id": self.blog.id,
                    "content": "<p>Test content</p>",
                }
            )
        )

    def test_action_open_backend_form(self):
        """Test that action_open_backend_form returns correct action."""
        # Test with single record (ensure_one is called)
        action = self.blog_post.action_open_backend_form()
        self.assertIsNotNone(action)
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "blog.post")
        self.assertEqual(action["res_id"], self.blog_post.id)
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["target"], "current")

    def test_visits_field_display(self):
        """Test that visits field is accessible and editable."""
        self.assertEqual(self.blog_post.visits, 0)
        # Update visits
        self.blog_post.visits = 10
        self.assertEqual(self.blog_post.visits, 10)
