# Copyright 2026 Domatix <info@domatix.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import json

from markupsafe import Markup

from odoo import models


class BlogPost(models.Model):
    _inherit = "blog.post"

    def _get_article_jsonld(self):
        """Build a schema.org BlogPosting JSON-LD block."""
        self.ensure_one()
        website = self.website_id or self.env["website"].get_current_website()
        base_url = website.get_base_url()
        slug = self.env["ir.http"]._slug
        url = f"{base_url}/blog/{slug(self.blog_id)}/{slug(self)}"
        logo_url = f"{base_url}/web/image/website/{website.id}/logo"
        og_img = self.website_meta_og_img
        if og_img and og_img.startswith("http"):
            image = og_img
        elif og_img:
            image = f"{base_url}/web/image/{og_img}"
        else:
            image = None
        date_published = self.post_date.isoformat() if self.post_date else None
        date_modified = self.write_date.isoformat() if self.write_date else None
        data = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": self.name or "",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": url,
            },
            "url": url,
            "datePublished": date_published,
            "dateModified": date_modified,
            "publisher": {
                "@type": "Organization",
                "name": website.name,
                "logo": {
                    "@type": "ImageObject",
                    "url": logo_url,
                },
            },
            "inLanguage": self.env.lang,
        }
        author_name = self.author_id.sudo().name
        if author_name:
            data["author"] = {"@type": "Person", "name": author_name}
        if image:
            data["image"] = image
        return Markup(json.dumps(data, ensure_ascii=False))
