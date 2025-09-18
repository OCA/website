# Copyright 2025 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.http_routing.models.ir_http import slug


class NewsletterToBlogpostWizard(models.TransientModel):
    _name = "newsletter.to.blogpost.wizard"
    _description = "Convert to Blogpost"

    publish = fields.Boolean(default=True)
    mailing_id = fields.Many2one("mailing.mailing", required=True)
    blog_id = fields.Many2one("blog.blog", required=True)
    tag_ids = fields.Many2many(
        comodel_name="blog.tag",
        required=True,
        default=lambda self: self.env["blog.tag"]
        .search([("name", "=", "General Newsletter")])
        .ids,
    )

    def newsletter_to_blogpost(self):
        self.ensure_one()
        new_blog_post = self.env["blog.post"].create(
            {
                "name": self.mailing_id.subject,
                "content": self.mailing_id.body_arch,
                "blog_id": self.blog_id.id,
                "tag_ids": self.tag_ids.ids,
                "is_published": self.publish,
            }
        )
        self.mailing_id.blog_post_id = new_blog_post.id
        return {
            "type": "ir.actions.act_url",
            "url": "/blog/%s/post/%s"
            % (slug(new_blog_post.blog_id), slug(new_blog_post)),
            "target": "self",
        }
