# Copyright 2024 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class WebsitePage(models.Model):
    _inherit = "website.page"

    is_redirect = fields.Boolean(
        string="Redirect",
        help="If checked, this page will redirect to another URL.",
    )
    redirect_url = fields.Char(
        string="Redirect URL",
        help="URL to redirect to when this page is accessed.",
    )
    redirect_method = fields.Selection(
        selection=[
            ("http", "HTTP"),
            ("meta", "Meta Refresh"),
            ("js-href", "JavaScript HREF"),
            ("js-replace", "JavaScript Replace"),
        ],
        default="http",
        help="Method to use for the redirect.",
    )
    redirect_http_code = fields.Selection(
        selection=[
            ("301", "301 Moved Permanently"),
            ("302", "302 Found"),
            ("303", "303 See Other"),
            ("307", "307 Temporary Redirect"),
            ("308", "308 Permanent Redirect"),
        ],
        string="Redirect HTTP Code",
        default="301",
        help="HTTP status code to use for the redirect.",
    )
    redirect_delay = fields.Integer(
        default=0,
        help=(
            "Delay before redirect (in seconds) for Meta-Refresh and JavaScript"
            " redirect methods."
        ),
    )
    redirect_js_code = fields.Html(
        compute="_compute_redirect_js_code",
        sanitize=False,
        string="Redirect JavaScript Code",
    )

    @api.depends("redirect_url", "redirect_delay", "redirect_method")
    def _compute_redirect_js_code(self):
        for page in self:
            if page.redirect_method not in ("js-href", "js-replace"):
                page.redirect_js_code = ""
                continue
            if page.redirect_method == "js-href":
                function_body = f"window.location.href = '{page.redirect_url}';"
            elif page.redirect_method == "js-replace":
                function_body = f"window.location.replace('{page.redirect_url}');"
            page.redirect_js_code = (
                '<script type="text/javascript">setTimeout(\n'
                f"    function() {{ {function_body} }},\n"
                f"    {page.redirect_delay * 1000},\n"
                ");</script>"
            )
