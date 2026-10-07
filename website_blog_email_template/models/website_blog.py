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

    def message_post_with_view(
        self, view_xmlid, subject=None, values=None, subtype_id=None, **kwargs
    ):
        render_values = values or {}
        return self.message_post_with_source(
            view_xmlid,
            subject=subject,
            render_values=render_values,
            subtype_id=subtype_id,
            **kwargs,
        )

    def message_post_with_template(
        self,
        template_id,
        subject=None,
        email_layout_xmlid=None,
        subtype_id=None,
        **kwargs,
    ):
        template = self.env["mail.template"].browse(template_id).sudo()

        for blog in self:
            subject_map = template._render_field("subject", [blog.id])
            body_map = template._render_field("body_html", [blog.id])

            final_subject = subject or subject_map.get(blog.id) or ""
            body = body_map.get(blog.id) or ""

            blog.message_post(
                body=body,
                subject=final_subject,
                subtype_id=subtype_id,
                **kwargs,
            )

        return self.message_ids[:1]


class BlogPost(models.Model):
    _inherit = "blog.post"

    def _check_for_publication(self, vals):
        if vals.get("is_published"):
            for post in self.filtered(lambda p: p.active):
                if post.blog_id.mail_template_id:
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
