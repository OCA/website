# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import re

from odoo import api, fields, models


class WebsitePage(models.Model):
    _inherit = "website.page"

    critical_css = fields.Text("Critical CSS")

    @api.model
    def get_page_info(self, id):
        return self.browse(id).read(
            [
                "id",
                "name",
                "url",
                "website_published",
                "website_indexed",
                "date_publish",
                "menu_ids",
                "is_homepage",
                "website_id",
                "critical_css",
            ],
        )

    def write(self, vals):
        if "critical_css" in vals:
            # strip wrapping spaces or style tags
            css = (vals.get("critical_css") or "").strip()
            lstrip = re.compile(r"^<\s*style\s*>\s*", re.IGNORECASE)
            rstrip = re.compile(r"\s*<\s*style\s*>$", re.IGNORECASE)
            vals["critical_css"] = re.sub(lstrip, "", re.sub(rstrip, "", css)) or None
        return super(WebsitePage, self).write(vals)
