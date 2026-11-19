# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request

from odoo.addons.html_editor.controllers.main import HTML_Editor

from ..tools import get_allowed_hosts, get_html5_video_url_data


class HTML5VideoEditor(HTML_Editor):
    @http.route()
    def video_url_data(
        self,
        video_url,
        autoplay=False,
        loop=False,
        hide_controls=False,
        hide_fullscreen=False,
        hide_dm_logo=False,
        hide_dm_share=False,
        start_from=False,
    ):
        res = super().video_url_data(
            video_url,
            autoplay=autoplay,
            loop=loop,
            hide_controls=hide_controls,
            hide_fullscreen=hide_fullscreen,
            hide_dm_logo=hide_dm_logo,
            hide_dm_share=hide_dm_share,
            start_from=start_from,
        )
        if not res.get("error"):
            return res
        return (
            get_html5_video_url_data(
                video_url,
                allowed_hosts=get_allowed_hosts(request.env),
                autoplay=autoplay,
                loop=loop,
                hide_controls=hide_controls,
                start_from=start_from,
            )
            or res
        )
