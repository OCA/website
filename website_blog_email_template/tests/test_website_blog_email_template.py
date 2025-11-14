# Copyright 2025 Marcel Savegnago - Escodoo <https://escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from unittest.mock import patch

from odoo.tests.common import tagged

from odoo.addons.website_blog.tests.common import TestWebsiteBlogCommon


@tagged("post_install", "-at_install")
class TestWebsiteBlogEmailTemplate(TestWebsiteBlogCommon):
    def setUp(self):
        super().setUp()
        self.mail_template = self.env["mail.template"].create(
            {
                "name": "Test Blog Post Template",
                "model_id": self.env["ir.model"]._get("blog.blog").id,
                "subject": "New post: {{ object.name }}",
                "body_html": "<p>New post {{ ctx.get('blog_post').name }} published!</p>",
            }
        )

    def test_blog_post_publication_without_template(self):
        """Test that default template is used when no custom template is configured"""
        blog = self.test_blog
        blog.mail_template_id = False

        # Subscribe users to the blog
        blog.message_subscribe(
            [self.user_employee.partner_id.id, self.user_public.partner_id.id]
        )

        # Create a new post
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Test Post Without Template",
                    "blog_id": blog.id,
                    "content": "<p>Test content</p>",
                }
            )
        )

        # Mock message_post_with_view to verify it's called
        with patch.object(
            type(blog), "message_post_with_view"
        ) as mock_message_post_with_view:
            # Publish the post
            post.write({"website_published": True})

            # Verify message_post_with_view was called with default template
            mock_message_post_with_view.assert_called_once()
            call_args = mock_message_post_with_view.call_args
            self.assertEqual(
                call_args[0][0], "website_blog.blog_post_template_new_post"
            )
            self.assertEqual(call_args[1]["subject"], "Test Post Without Template")
            self.assertIn("post", call_args[1]["values"])
            self.assertEqual(call_args[1]["values"]["post"], post)

    def test_blog_post_publication_with_template(self):
        """Test that custom template is used when configured"""
        blog = self.test_blog
        blog.mail_template_id = self.mail_template

        # Subscribe users to the blog
        blog.message_subscribe(
            [self.user_employee.partner_id.id, self.user_public.partner_id.id]
        )

        # Create a new post
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Test Post With Template",
                    "blog_id": blog.id,
                    "content": "<p>Test content</p>",
                }
            )
        )

        # Mock message_post_with_template to verify it's called
        with patch.object(
            type(blog), "message_post_with_template"
        ) as mock_message_post_with_template:
            # Publish the post
            post.write({"website_published": True})

            # Verify message_post_with_template was called with custom template
            mock_message_post_with_template.assert_called_once()
            call_args = mock_message_post_with_template.call_args
            self.assertEqual(call_args[0][0], self.mail_template.id)
            self.assertEqual(call_args[1]["subject"], "Test Post With Template")
            self.assertEqual(
                call_args[1]["email_layout_xmlid"], "mail.mail_notification_light"
            )

    def test_blog_post_publication_context(self):
        """Test that blog post is passed in context when using custom template"""
        blog = self.test_blog
        blog.mail_template_id = self.mail_template

        # Subscribe users to the blog
        blog.message_subscribe(
            [self.user_employee.partner_id.id, self.user_public.partner_id.id]
        )

        # Create a new post
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Test Post Context",
                    "blog_id": blog.id,
                    "content": "<p>Test content</p>",
                }
            )
        )

        # Track context passed to message_post_with_template
        captured_context = {}

        # Store original method
        original_message_post_with_template = type(blog).message_post_with_template

        def mock_message_post_with_template(self, *args, **kwargs):
            # Capture context from the recordset that calls the method
            # (self is the recordset returned by with_context)
            captured_context["context"] = self.env.context
            # Call original method
            return original_message_post_with_template(self, *args, **kwargs)

        # Patch message_post_with_template to capture context
        with patch.object(
            type(blog), "message_post_with_template", mock_message_post_with_template
        ):
            # Publish the post
            post.write({"website_published": True})

            # Verify context contains blog_post
            self.assertIn("blog_post", captured_context["context"])
            self.assertIn("blog_post_id", captured_context["context"])
            self.assertEqual(captured_context["context"]["blog_post"], post)
            self.assertEqual(captured_context["context"]["blog_post_id"], post.id)

    def test_blog_post_publication_message_creation(self):
        """Test that messages are actually created when publishing posts"""
        blog = self.test_blog
        blog.mail_template_id = False

        # Subscribe users to the blog
        blog.message_subscribe(
            [self.user_employee.partner_id.id, self.user_public.partner_id.id]
        )

        # Count initial messages
        initial_message_count = len(blog.message_ids)

        # Create and publish a post
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Test Post Message",
                    "blog_id": blog.id,
                    "content": "<p>Test content</p>",
                }
            )
        )
        post.write({"website_published": True})

        # Verify a new message was created
        self.assertEqual(len(blog.message_ids), initial_message_count + 1)

        # Verify the message has the correct subtype
        publish_message = blog.message_ids.filtered(
            lambda m: m.subtype_id
            == self.env.ref("website_blog.mt_blog_blog_published")
        )
        self.assertTrue(publish_message, "Publish message should be created")

        # Verify followers are notified
        self.assertIn(
            self.user_employee.partner_id,
            publish_message.notified_partner_ids,
            "Blog followers should be notified",
        )

    def test_blog_post_publication_with_template_message_creation(self):
        """Test that messages are created when using custom template"""
        blog = self.test_blog
        blog.mail_template_id = self.mail_template

        # Subscribe users to the blog
        blog.message_subscribe(
            [self.user_employee.partner_id.id, self.user_public.partner_id.id]
        )

        # Count initial messages
        initial_message_count = len(blog.message_ids)

        # Create and publish a post
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Test Post Custom Template",
                    "blog_id": blog.id,
                    "content": "<p>Test content</p>",
                }
            )
        )
        post.write({"website_published": True})

        # Verify a new message was created
        self.assertEqual(len(blog.message_ids), initial_message_count + 1)

        # Verify the message has the correct subtype
        publish_message = blog.message_ids.filtered(
            lambda m: m.subtype_id
            == self.env.ref("website_blog.mt_blog_blog_published")
        )
        self.assertTrue(publish_message, "Publish message should be created")

        # Verify followers are notified
        self.assertIn(
            self.user_employee.partner_id,
            publish_message.notified_partner_ids,
            "Blog followers should be notified",
        )

    def test_blog_post_unpublish_no_notification(self):
        """Test that unpublishing a post doesn't trigger notification"""
        blog = self.test_blog
        blog.mail_template_id = False

        # Subscribe users to the blog
        blog.message_subscribe(
            [self.user_employee.partner_id.id, self.user_public.partner_id.id]
        )

        # Create and publish a post
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Test Post Unpublish",
                    "blog_id": blog.id,
                    "content": "<p>Test content</p>",
                }
            )
        )
        post.write({"website_published": True})

        # Count messages after publishing
        messages_after_publish = len(blog.message_ids)

        # Unpublish the post
        post.write({"website_published": False})

        # Verify no new message was created
        self.assertEqual(len(blog.message_ids), messages_after_publish)
