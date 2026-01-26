# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestBlogPostScheduledPublication(TransactionCase):
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

    def test_scheduled_publication_future_date(self):
        """Test that a post with future scheduled date is not published immediately."""
        future_date = fields.Datetime.now() + timedelta(days=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Scheduled Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date,
                    "website_published": True,  # Try to publish immediately
                }
            )
        )
        # Post should not be published because of future scheduled date
        self.assertFalse(
            post.website_published,
            "Post with future scheduled date should not be published immediately",
        )
        self.assertEqual(
            post.scheduled_publication_date,
            future_date,
            "Scheduled date should be preserved",
        )

    def test_scheduled_publication_past_date(self):
        """Test that a post with past scheduled date is published immediately."""
        past_date = fields.Datetime.now() - timedelta(days=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Past Scheduled Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": past_date,
                    "website_published": True,
                }
            )
        )
        # Post should be published immediately and scheduled date cleared
        self.assertTrue(
            post.website_published,
            "Post with past scheduled date should be published immediately",
        )
        self.assertFalse(
            post.scheduled_publication_date,
            "Past scheduled date should be cleared after publication",
        )

    def test_scheduled_publication_no_date(self):
        """Test that a post without scheduled date is published immediately."""
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Immediate Post",
                    "blog_id": self.blog.id,
                    "website_published": True,
                }
            )
        )
        # Post should be published immediately
        self.assertTrue(
            post.website_published,
            "Post without scheduled date should be published immediately",
        )
        self.assertFalse(
            post.scheduled_publication_date,
            "Post without scheduled date should have no scheduled date",
        )

    def test_scheduled_publication_set_future_date_on_published_post(self):
        """Test that setting a future date on a published post unpublishes it."""
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Published Post",
                    "blog_id": self.blog.id,
                    "website_published": True,
                }
            )
        )
        self.assertTrue(post.website_published, "Post should be published")

        # Set a future scheduled date
        future_date = fields.Datetime.now() + timedelta(days=1)
        post.with_context(mail_create_nolog=True).write(
            {"scheduled_publication_date": future_date}
        )

        # Post should be unpublished
        self.assertFalse(
            post.website_published,
            "Post should be unpublished when future scheduled date is set",
        )
        self.assertEqual(
            post.scheduled_publication_date,
            future_date,
            "Scheduled date should be set",
        )

    def test_scheduled_publication_clear_future_date(self):
        """Test that clearing a future scheduled date allows immediate publication."""
        future_date = fields.Datetime.now() + timedelta(days=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Scheduled Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date,
                }
            )
        )
        self.assertFalse(post.website_published, "Post should not be published")

        # Clear scheduled date and publish
        post.with_context(mail_create_nolog=True).write(
            {"scheduled_publication_date": False, "website_published": True}
        )

        # Post should be published
        self.assertTrue(
            post.website_published,
            "Post should be published when scheduled date is cleared",
        )
        self.assertFalse(
            post.scheduled_publication_date,
            "Scheduled date should be cleared",
        )

    def test_cron_publish_scheduled_posts(self):
        """Test that cron job publishes scheduled posts when date arrives."""
        # Count initial messages on blog
        initial_message_count = len(self.blog.message_ids)

        # Create posts with past scheduled dates
        past_date = fields.Datetime.now() - timedelta(hours=1)
        scheduled_post1 = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Scheduled Post 1",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": past_date,
                    "website_published": False,
                }
            )
        )
        scheduled_post2 = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Scheduled Post 2",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": past_date,
                    "website_published": False,
                }
            )
        )

        # Create a post with future scheduled date (should not be published)
        future_date = fields.Datetime.now() + timedelta(days=1)
        future_post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Future Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date,
                    "website_published": False,
                }
            )
        )

        # Run the cron job
        self.env["blog.post"]._publish_scheduled_posts()

        # Past scheduled posts should be published
        self.assertTrue(
            scheduled_post1.website_published,
            "Past scheduled post should be published by cron",
        )
        self.assertFalse(
            scheduled_post1.scheduled_publication_date,
            "Scheduled date should be cleared after publication",
        )

        self.assertTrue(
            scheduled_post2.website_published,
            "Past scheduled post should be published by cron",
        )
        self.assertFalse(
            scheduled_post2.scheduled_publication_date,
            "Scheduled date should be cleared after publication",
        )

        # Future post should not be published
        self.assertFalse(
            future_post.website_published,
            "Future scheduled post should not be published by cron",
        )
        self.assertEqual(
            future_post.scheduled_publication_date,
            future_date,
            "Future scheduled date should be preserved",
        )

        # Verify that notifications were sent (messages should be created on blog)
        # Each published post should create a notification message
        final_message_count = len(self.blog.message_ids)
        self.assertGreater(
            final_message_count,
            initial_message_count,
            "Notifications should be sent when posts are published by cron",
        )

    def test_cron_skip_inactive_posts(self):
        """Test that cron job skips inactive posts."""
        past_date = fields.Datetime.now() - timedelta(hours=1)
        inactive_post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Inactive Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": past_date,
                    "website_published": False,
                    "active": False,
                }
            )
        )

        # Run the cron job
        self.env["blog.post"]._publish_scheduled_posts()

        # Inactive post should not be published
        self.assertFalse(
            inactive_post.website_published,
            "Inactive post should not be published by cron",
        )

    def test_cron_skip_already_published_posts(self):
        """Test that cron job skips already published posts."""
        past_date = fields.Datetime.now() - timedelta(hours=1)
        published_post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Already Published Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": past_date,
                    "website_published": True,
                }
            )
        )

        # Run the cron job
        self.env["blog.post"]._publish_scheduled_posts()

        # Post should remain published
        self.assertTrue(
            published_post.website_published,
            "Already published post should remain published",
        )

    def test_scheduled_publication_string_to_datetime_conversion(self):
        """Test that string dates are properly converted to datetime."""
        future_date = fields.Datetime.now() + timedelta(days=1)
        future_date_str = fields.Datetime.to_string(future_date)

        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "String Date Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date_str,
                    "website_published": True,
                }
            )
        )

        # Post should not be published because of future scheduled date
        self.assertFalse(
            post.website_published,
            "Post with future scheduled date (string) should not be published",
        )
        # Scheduled date should be stored and not False
        self.assertTrue(
            post.scheduled_publication_date,
            "Scheduled date should be stored",
        )
        # Verify the date is correct (allowing for small time differences)
        stored_date = fields.Datetime.from_string(
            fields.Datetime.to_string(post.scheduled_publication_date)
        )
        expected_date = fields.Datetime.from_string(future_date_str)
        self.assertEqual(
            stored_date,
            expected_date,
            "Scheduled date should match the original date",
        )

    def test_write_without_scheduled_date_or_publication(self):
        """Test that write without scheduled date or publication uses standard write."""
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Test Post",
                    "blog_id": self.blog.id,
                }
            )
        )
        # Write without scheduled date or publication should work normally
        post.write({"name": "Updated Post Name"})
        self.assertEqual(post.name, "Updated Post Name")

    def test_write_set_past_date_on_unpublished_post(self):
        """Test that setting a past date on unpublished post clears the date."""
        future_date = fields.Datetime.now() + timedelta(days=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Scheduled Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date,
                    "website_published": False,
                }
            )
        )
        # Set a past date
        past_date = fields.Datetime.now() - timedelta(hours=1)
        post.write({"scheduled_publication_date": past_date})

        # Past date should be cleared
        self.assertFalse(
            post.scheduled_publication_date,
            "Past scheduled date should be cleared when set on unpublished post",
        )

    def test_write_publish_with_existing_past_scheduled_date(self):
        """Test publishing a post that has an existing past scheduled date."""
        past_date = fields.Datetime.now() - timedelta(hours=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Post with Past Date",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": past_date,
                    "website_published": False,
                }
            )
        )
        # Publish the post (scheduled date exists but not in vals)
        post.with_context(mail_create_nolog=True).write({"website_published": True})

        # Post should be published and scheduled date cleared
        self.assertTrue(
            post.website_published,
            "Post should be published when publishing with existing past scheduled date",
        )
        self.assertFalse(
            post.scheduled_publication_date,
            "Past scheduled date should be cleared after publication",
        )

    def test_write_multiple_records_different_scheduled_dates(self):
        """Test write with multiple records having different scheduled dates."""
        future_date = fields.Datetime.now() + timedelta(days=1)
        past_date = fields.Datetime.now() - timedelta(hours=1)

        post1 = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Post 1",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date,
                    "website_published": False,
                }
            )
        )
        post2 = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Post 2",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": past_date,
                    "website_published": False,
                }
            )
        )

        # Try to publish both posts
        posts = post1 | post2
        posts.with_context(mail_create_nolog=True).write({"website_published": True})

        # Post1 should not be published (future date)
        self.assertFalse(
            post1.website_published,
            "Post with future scheduled date should not be published",
        )
        # Post2 should be published (past date)
        self.assertTrue(
            post2.website_published,
            "Post with past scheduled date should be published",
        )
        self.assertFalse(
            post2.scheduled_publication_date,
            "Past scheduled date should be cleared after publication",
        )

    def test_create_with_past_date_not_publishing(self):
        """Test creating a post with past date but not publishing."""
        past_date = fields.Datetime.now() - timedelta(hours=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Post with Past Date",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": past_date,
                    "website_published": False,
                }
            )
        )
        # Past date should be kept for cron to handle
        self.assertFalse(post.website_published, "Post should not be published")
        self.assertEqual(
            post.scheduled_publication_date,
            past_date,
            "Past scheduled date should be preserved when not publishing",
        )

    def test_create_with_future_date_not_publishing(self):
        """Test creating a post with future date but not publishing."""
        future_date = fields.Datetime.now() + timedelta(days=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Post with Future Date",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date,
                    "website_published": False,
                }
            )
        )
        # Future date should be kept
        self.assertFalse(post.website_published, "Post should not be published")
        self.assertEqual(
            post.scheduled_publication_date,
            future_date,
            "Future scheduled date should be preserved",
        )

    def test_write_set_past_date_on_published_post(self):
        """Test that setting a past date on published post publishes immediately."""
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Published Post",
                    "blog_id": self.blog.id,
                    "website_published": True,
                }
            )
        )
        # Set a past scheduled date
        past_date = fields.Datetime.now() - timedelta(hours=1)
        post.with_context(mail_create_nolog=True).write(
            {"scheduled_publication_date": past_date}
        )

        # Post should remain published and scheduled date cleared
        self.assertTrue(
            post.website_published,
            "Post should remain published when past date is set",
        )
        self.assertFalse(
            post.scheduled_publication_date,
            "Past scheduled date should be cleared",
        )

    def test_cron_empty_result(self):
        """Test that cron handles empty result gracefully."""
        # Run cron when there are no scheduled posts
        result = self.env["blog.post"]._publish_scheduled_posts()
        self.assertTrue(result, "Cron should return True even with no posts")

    def test_check_for_publication_sends_notifications(self):
        """Test that _check_for_publication sends notifications to blog followers."""
        # Count initial messages on blog
        initial_message_count = len(self.blog.message_ids)

        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Test Post",
                    "blog_id": self.blog.id,
                    "website_published": False,
                }
            )
        )

        # Call _check_for_publication directly
        result = post._check_for_publication({"is_published": True})
        self.assertTrue(result, "Should return True when publishing")

        # Verify that notification message was created on blog
        final_message_count = len(self.blog.message_ids)
        self.assertGreater(
            final_message_count,
            initial_message_count,
            "Notification should be sent when post is published",
        )

    def test_action_publish_now(self):
        """Test action_publish_now method publishes immediately."""
        future_date = fields.Datetime.now() + timedelta(days=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Scheduled Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date,
                    "is_scheduled": True,
                    "website_published": False,
                }
            )
        )
        self.assertFalse(post.website_published)
        self.assertTrue(post.is_scheduled)

        # Call action_publish_now
        post.with_context(mail_create_nolog=True).action_publish_now()

        # Post should be published immediately
        self.assertTrue(
            post.website_published,
            "Post should be published after action_publish_now",
        )
        self.assertFalse(
            post.is_scheduled,
            "is_scheduled should be False after action_publish_now",
        )
        self.assertFalse(
            post.scheduled_publication_date,
            "Scheduled date should be cleared after action_publish_now",
        )

    def test_action_schedule(self):
        """Test action_schedule method returns the correct action."""
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Test Post",
                    "blog_id": self.blog.id,
                    "website_published": False,
                }
            )
        )

        # Call action_schedule
        action = post.action_schedule()

        # Verify action structure
        self.assertEqual(
            action["res_model"],
            "blog.post.schedule.date",
            "Action should target blog.post.schedule.date wizard",
        )
        self.assertEqual(
            action["context"]["default_blog_post_id"],
            post.id,
            "Action context should include default_blog_post_id",
        )
        self.assertEqual(
            action["context"]["dialog_size"],
            "medium",
            "Action context should include dialog_size",
        )

    def test_action_schedule_with_existing_date(self):
        """Test action_schedule with existing scheduled date."""
        future_date = fields.Datetime.now() + timedelta(days=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Scheduled Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date,
                    "website_published": False,
                }
            )
        )

        # Call action_schedule
        action = post.action_schedule()

        # Verify action context includes existing scheduled date
        self.assertEqual(
            action["context"]["default_schedule_date"],
            future_date,
            "Action context should include existing scheduled date",
        )

    def test_wizard_action_schedule_date(self):
        """Test the wizard action_schedule_date method."""
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Test Post",
                    "blog_id": self.blog.id,
                    "website_published": False,
                }
            )
        )

        future_date = fields.Datetime.now() + timedelta(days=2)
        wizard = self.env["blog.post.schedule.date"].create(
            {
                "blog_post_id": post.id,
                "schedule_date": future_date,
            }
        )

        # Call action_schedule_date
        result = wizard.action_schedule_date()

        # Verify return value
        self.assertTrue(result, "Wizard should return True")

        # Verify post was updated
        self.assertTrue(
            post.is_scheduled,
            "Post is_scheduled should be True",
        )
        self.assertEqual(
            post.scheduled_publication_date,
            future_date,
            "Post scheduled_publication_date should be set",
        )
        self.assertFalse(
            post.website_published,
            "Post should not be published",
        )

    def test_is_scheduled_change_to_scheduled(self):
        """Test changing is_scheduled to 'scheduled' sets a default date."""
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Test Post",
                    "blog_id": self.blog.id,
                    "website_published": False,
                }
            )
        )
        self.assertFalse(post.is_scheduled)
        self.assertFalse(post.scheduled_publication_date)

        # Change is_scheduled to True
        post.write({"is_scheduled": True})

        # Should set a default future date (tomorrow)
        self.assertTrue(post.is_scheduled)
        self.assertIsNotNone(post.scheduled_publication_date)
        self.assertGreater(
            post.scheduled_publication_date,
            fields.Datetime.now(),
            "Default scheduled date should be in the future",
        )

    def test_is_scheduled_change_to_now(self):
        """Test changing is_scheduled to False clears the date."""
        future_date = fields.Datetime.now() + timedelta(days=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Scheduled Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date,
                    "is_scheduled": True,
                    "website_published": False,
                }
            )
        )
        self.assertTrue(post.is_scheduled)
        self.assertEqual(post.scheduled_publication_date, future_date)

        # Change is_scheduled to False
        post.write({"is_scheduled": False})

        # Should clear the scheduled date
        self.assertFalse(post.is_scheduled)
        self.assertFalse(post.scheduled_publication_date)

    def test_check_for_publication_with_future_scheduled_date(self):
        """Test _check_for_publication skips posts with future scheduled date."""
        future_date = fields.Datetime.now() + timedelta(days=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Scheduled Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date,
                    "website_published": False,
                }
            )
        )

        # Call _check_for_publication
        result = post._check_for_publication({"is_published": True})

        # Should return False (no notifications for future scheduled posts)
        self.assertFalse(
            result,
            "Should return False for posts with future scheduled date",
        )

    def test_check_for_publication_not_publishing(self):
        """Test _check_for_publication returns False when not publishing."""
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Test Post",
                    "blog_id": self.blog.id,
                    "website_published": False,
                }
            )
        )

        # Call _check_for_publication without is_published
        result = post._check_for_publication({})

        # Should return False
        self.assertFalse(
            result,
            "Should return False when not publishing",
        )

    def test_check_for_publication_with_future_date_in_vals(self):
        """Test _check_for_publication skips when future date is in vals."""
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .create(
                {
                    "name": "Test Post",
                    "blog_id": self.blog.id,
                    "website_published": False,
                }
            )
        )

        future_date = fields.Datetime.now() + timedelta(days=1)
        future_date_str = fields.Datetime.to_string(future_date)

        # Call _check_for_publication with future date in vals
        result = post._check_for_publication(
            {"is_published": True, "scheduled_publication_date": future_date_str}
        )

        # Should return False
        self.assertFalse(
            result,
            "Should return False when future scheduled date is in vals",
        )

    def test_write_clear_scheduled_date(self):
        """Test writing scheduled_publication_date to False clears it."""
        future_date = fields.Datetime.now() + timedelta(days=1)
        post = (
            self.env["blog.post"]
            .with_user(self.user_blogmanager)
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Scheduled Post",
                    "blog_id": self.blog.id,
                    "scheduled_publication_date": future_date,
                    "is_scheduled": True,
                    "website_published": False,
                }
            )
        )

        # Clear the scheduled date
        post.write({"scheduled_publication_date": False})

        # Should be cleared and is_scheduled set to now
        self.assertFalse(post.scheduled_publication_date)
        self.assertFalse(post.is_scheduled)
