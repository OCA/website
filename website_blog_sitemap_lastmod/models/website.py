# Copyright 2026 Domatix <info@domatix.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models


class Website(models.Model):
    _inherit = "website"

    def _enumerate_pages(self, query_string=None, force=False):
        """Add a trustworthy <lastmod> to blog.post URLs in the sitemap.

        Odoo core only emits lastmod for static website.page records; dynamic
        controller routes (blog posts included) are enumerated without a date.
        This override injects lastmod for blog.post URLs using the record
        write_date, which is reliable for posts because all the renderable
        content lives on the record itself (Odoo core pattern, commit fde2601,
        website_forum).

        We preload once a {url: lastmod} map for published posts so the
        enumeration stays single-query for the whole blog section.
        """
        posts = self.env["blog.post"].search_fetch(
            [("is_published", "=", True)],
            ["name", "write_date", "blog_id"],
        )
        slug = self.env["ir.http"]._slug
        lastmod_map = {
            f"/blog/{slug(p.blog_id)}/{slug(p)}": p.write_date.date()
            for p in posts
            if p.write_date
        }

        for page in super()._enumerate_pages(query_string=query_string, force=force):
            if page.get("lastmod"):
                yield page
                continue
            loc = page["loc"]
            if loc in lastmod_map:
                yield {**page, "lastmod": lastmod_map[loc]}
            else:
                yield page
