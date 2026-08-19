# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @api.model
    def get_frontend_session_info(self):
        # Used for the visibility of the website snippets
        session_info = super().get_frontend_session_info()
        if request.env.user.has_group("base.group_user"):
            session_info["user_group"] = "internal"
        elif request.env.user.has_group("base.group_portal"):
            session_info["user_group"] = "portal"
        else:
            session_info["user_group"] = "public"
        return session_info
