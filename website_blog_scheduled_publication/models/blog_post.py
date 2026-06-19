# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class BlogPost(models.Model):
    _inherit = "blog.post"

    scheduled_publication_date = fields.Datetime(
        help="If set, the blog post will be automatically published on "
        "this date and time. Leave empty to publish immediately.",
    )
    is_scheduled = fields.Boolean(
        string="Schedule",
        default=False,
        help="If checked, the blog post will be scheduled for publication.",
    )

    @api.model
    def _publish_scheduled_posts(self):
        """Cron job method to publish scheduled blog posts."""
        now = fields.Datetime.now()
        scheduled_posts = self.search(
            [
                ("scheduled_publication_date", "<=", now),
                ("scheduled_publication_date", "!=", False),
                ("website_published", "=", False),
                ("active", "=", True),
            ]
        )
        if scheduled_posts:
            scheduled_posts.write({"is_published": True})
            scheduled_posts.write(
                {"scheduled_publication_date": False, "is_scheduled": False}
            )
        return True

    def action_publish_now(self):
        """Publish the blog post immediately."""
        self.write(
            {
                "is_scheduled": False,
                "scheduled_publication_date": False,
                "is_published": True,
            }
        )
        return True

    def action_schedule(self):
        """Open schedule dialog to set publication date."""
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "website_blog_scheduled_publication.blog_post_schedule_date_action"
        )
        action["context"] = dict(
            self.env.context,
            default_blog_post_id=self.id,
            default_schedule_date=self.scheduled_publication_date or False,
            dialog_size="medium",
        )
        return action

    def _check_for_publication(self, vals):
        """Override to handle publication notifications properly.

        Skip notifications for posts that are scheduled for the future.
        Use sudo() to ensure notifications can be sent regardless of user
        permissions, as this is a system action that should always succeed.
        """
        if not vals.get("is_published"):
            return False

        now = fields.Datetime.now()
        posts_to_notify = self.filtered(
            lambda p: not self._has_future_scheduled_date(p, vals, now)
        )
        if not posts_to_notify:
            return False
        return super(BlogPost, posts_to_notify.sudo())._check_for_publication(vals)

    def _has_future_scheduled_date(self, post, vals, now):
        """Check if post has a future scheduled date."""
        if post.scheduled_publication_date and post.scheduled_publication_date > now:
            return True
        scheduled_date = fields.Datetime.from_string(
            vals.get("scheduled_publication_date")
        )
        return scheduled_date and scheduled_date > now

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to handle scheduled publication during creation."""
        now = fields.Datetime.now()
        processed_vals_list = []
        for vals in vals_list:
            processed_vals = self._process_create_vals(vals, now)
            processed_vals_list.append(processed_vals)
        return super().create(processed_vals_list)

    def _process_create_vals(self, vals, now):
        """Process vals for create to handle scheduled dates."""
        processed_vals = vals.copy()
        if "scheduled_publication_date" not in processed_vals:
            return processed_vals

        scheduled_date = fields.Datetime.from_string(
            processed_vals.get("scheduled_publication_date")
        )
        if scheduled_date and scheduled_date > now:
            if processed_vals.get("website_published"):
                processed_vals["website_published"] = False
        elif scheduled_date and scheduled_date <= now:
            if processed_vals.get("website_published"):
                processed_vals["scheduled_publication_date"] = False
        return processed_vals

    def write(self, vals):
        """Override write to handle scheduled publication logic."""
        relevant_fields = {
            "scheduled_publication_date",
            "website_published",
            "is_scheduled",
        }
        if not relevant_fields.intersection(vals.keys()):
            return super().write(vals)

        now = fields.Datetime.now()
        for record in self:
            record_vals = self._process_write_vals(record, vals, now)
            super(BlogPost, record.with_context(**self.env.context)).write(record_vals)
        return True

    def _process_write_vals(self, record, vals, now):
        """Process vals for write to handle scheduled publication logic."""
        record_vals = vals.copy()
        scheduled_date = self._get_effective_scheduled_date(record, record_vals)

        self._handle_is_scheduled_change(record_vals, scheduled_date, now)
        self._handle_scheduled_date_change(record, record_vals, now)
        self._handle_publication_request(record, record_vals, scheduled_date, now)

        return record_vals

    def _get_effective_scheduled_date(self, record, vals):
        """Get the scheduled date that will be effective after write."""
        if "scheduled_publication_date" in vals:
            return fields.Datetime.from_string(vals.get("scheduled_publication_date"))
        return fields.Datetime.from_string(record.scheduled_publication_date)

    def _handle_is_scheduled_change(self, vals, scheduled_date, now):
        """Handle is_scheduled field changes."""
        if "is_scheduled" not in vals:
            return

        if not vals["is_scheduled"]:
            vals["scheduled_publication_date"] = False
        else:
            if "scheduled_publication_date" not in vals:
                if not scheduled_date or scheduled_date <= now:
                    vals["scheduled_publication_date"] = now + relativedelta(days=1)

    def _handle_scheduled_date_change(self, record, vals, now):
        """Handle scheduled_publication_date field changes."""
        if "scheduled_publication_date" not in vals:
            return

        new_date_raw = vals.get("scheduled_publication_date")
        new_date = fields.Datetime.from_string(new_date_raw)

        if new_date and new_date > now:
            self._set_future_scheduled_date(record, vals, new_date_raw)
        elif new_date and new_date <= now:
            vals["scheduled_publication_date"] = False
            vals.setdefault("is_scheduled", False)
        elif not new_date:
            vals.setdefault("is_scheduled", False)

    def _set_future_scheduled_date(self, record, vals, new_date_raw):
        """Set a future scheduled date and unpublish if needed."""
        will_be_published = vals.get("website_published", record.website_published)
        if will_be_published:
            vals["website_published"] = False
        vals.setdefault("is_scheduled", True)
        vals["scheduled_publication_date"] = new_date_raw

    def _handle_publication_request(self, record, vals, scheduled_date, now):
        """Handle publication request when website_published is being set."""
        if "website_published" not in vals or not vals.get("website_published"):
            return

        if scheduled_date and scheduled_date > now:
            vals["website_published"] = False
            vals.setdefault("scheduled_publication_date", scheduled_date)
            vals.setdefault("is_scheduled", True)
        elif scheduled_date and scheduled_date <= now:
            vals["scheduled_publication_date"] = False
            vals.setdefault("is_scheduled", False)
        else:
            vals.setdefault("is_scheduled", False)
