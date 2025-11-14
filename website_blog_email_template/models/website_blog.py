# Copyright 2025 Marcel Savegnago - Escodoo <https://escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Blog(models.Model):
    _inherit = "blog.blog"

    mail_template_id = fields.Many2one(
        comodel_name="mail.template",
        string="Email Template for New Posts",
        domain=[("model", "=", "blog.blog")],
        help="If set, this email template will be used when a new post is published "
        "instead of the default template. The template should be configured for "
        "the 'blog.blog' model.",
    )


class BlogPost(models.Model):
    _inherit = "blog.post"

    def _check_for_publication(self, vals):
        if vals.get("is_published"):
            for post in self.filtered(lambda p: p.active):
                # Use custom template if configured, otherwise use default
                if post.blog_id.mail_template_id:
                    # Use mail template with post in context
                    post.blog_id.with_context(
                        blog_post_id=post.id,
                        blog_post=post,
                    ).message_post_with_template(
                        post.blog_id.mail_template_id.id,
                        subject=post.name,
                        email_layout_xmlid="mail.mail_notification_light",
                        subtype_id=self.env["ir.model.data"]._xmlid_to_res_id(
                            "website_blog.mt_blog_blog_published"
                        ),
                    )
                else:
                    # Use default view template
                    post.blog_id.message_post_with_view(
                        "website_blog.blog_post_template_new_post",
                        subject=post.name,
                        values={"post": post},
                        subtype_id=self.env["ir.model.data"]._xmlid_to_res_id(
                            "website_blog.mt_blog_blog_published"
                        ),
                    )
            return True
        return False
