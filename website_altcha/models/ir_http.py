# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import hashlib
import hmac
import json
import logging

import altcha.v2 as altcha

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @api.model
    def get_frontend_session_info(self):
        frontend_session_info = super().get_frontend_session_info()
        return self._add_altcha_public_key_to_session_info(frontend_session_info)

    @api.model
    def _add_altcha_public_key_to_session_info(self, session_info):
        """Add the Altcha public key to the given session_info object"""
        session_info["altcha_public_key"] = bool(request.website.sudo().altcha_key)
        return session_info

    @api.model
    def _get_altcha_key(self, signature):
        return hmac.new(
            signature.encode("utf-8"),
            request.httprequest.remote_addr.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

    @api.model
    def _verify_request_recaptcha_token(self, action):
        result = super()._verify_request_recaptcha_token(action)
        if not result:
            return result
        if not request.website.sudo().altcha_key:
            return result
        altcha_signature = request.params.get("altcha")
        if not altcha_signature:
            _logger.warning("Altcha token missing in request")
            raise UserError(_("Suspicious activity detected by Altcha"))
        result = altcha.verify_solution(
            altcha_signature,
            hmac_secret=request.website.sudo().altcha_key,
            hmac_key_secret=request.website.sudo().altcha_private_key,
        )
        is_valid = result.verified
        if not is_valid:
            error = []
            if result.invalid_signature:
                error.append("Invalid Signature")
            if result.invalid_solution:
                error.append("Invalid Solution")
            if result.expired:
                error.append("Expired")
            if result.error:
                error.append(result.error)
            _logger.warning(
                """Altcha verification failed: %s""",
                ", ".join(error),
            )
            raise UserError(_("Suspicious activity detected by Altcha"))
        altcha_request = json.loads(base64.b64decode(altcha_signature))
        unique_id = self._get_altcha_key(altcha_request["challenge"]["signature"])
        record = (
            self.env["altcha.key"]
            .sudo()
            .search(
                [
                    ("key", "=", unique_id),
                    ("used", "=", False),
                ],
                limit=1,
            )
        )
        if not record:
            _logger.warning(f"Altcha key not found or already used: {unique_id}")
            raise UserError(_("Suspicious activity detected by Altcha"))
        record.used = True
        return result
