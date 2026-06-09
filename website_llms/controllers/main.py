# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import http
from odoo.http import request


class LlmsTxtController(http.Controller):
    @http.route(
        "/llms.txt",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
        methods=["GET"],
        csrf=False,
    )
    def llms_txt(self, **kwargs):
        """
        Serve the llms.txt file with content configured in website settings.
        If no content is configured, returns a default message.
        """
        website = request.website
        content = website.llms_txt_content or ""

        # If content is empty, return a default message
        if not content.strip():
            base_url = website.domain or request.httprequest.host_url.rstrip("/")
            content = f"""# {website.name} — Information for LLMs

## Company
- Website: {base_url}
- About: {base_url}/aboutus
- Contact: {base_url}/contactus

## Content
- Blog: {base_url}/blog
"""

        # Ensure content ends with a newline
        content = content.strip() + "\n"

        headers = [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Cache-Control", "public, max-age=3600"),
        ]

        return request.make_response(content, headers=headers)
