from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _dispatch(cls):
        response = super(IrHttp, cls)._dispatch()
        if request.is_frontend:
            website = request.website
            path = request.httprequest.path
            if not request.env.user.has_group("website.group_website_designer"):
                matching_triggers = (
                    request.env["ab.testing.target.trigger"]
                    .sudo()
                    .search(
                        [
                            ("target_id.website_id", "=", website.id),
                            ("on", "=", "url_visit"),
                            ("url", "=", path),
                        ]
                    )
                )
                matching_triggers.create_conversion()
        return response
