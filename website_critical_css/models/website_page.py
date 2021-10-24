# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
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
            css = vals.get("critical_css")
            css = css.replace("<style>", "").replace("</style>", "")
            vals["critical_css"] = css
        return super(WebsitePage, self).write(vals)
