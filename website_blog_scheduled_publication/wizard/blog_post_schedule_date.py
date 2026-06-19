# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BlogPostScheduleDate(models.TransientModel):
    _name = "blog.post.schedule.date"
    _description = "Schedule a blog post publication"

    schedule_date = fields.Datetime(string="Publish on", required=True)
    blog_post_id = fields.Many2one("blog.post", required=True)

    def action_schedule_date(self):
        """Schedule the blog post for publication."""
        self.blog_post_id.write(
            {
                "is_scheduled": True,
                "scheduled_publication_date": self.schedule_date,
                "website_published": False,
            }
        )
        return True
