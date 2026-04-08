# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import hashlib
import hmac
import json
import logging

import altcha.v1 as altcha

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        session_info = super().session_info()
        return self._add_altcha_public_key_to_session_info(session_info)

    @api.model
    def get_frontend_session_info(self):
        frontend_session_info = super().get_frontend_session_info()
        return self._add_altcha_public_key_to_session_info(frontend_session_info)

    @api.model
    def _add_altcha_public_key_to_session_info(self, session_info):
        """Add the Altcha public key to the given session_info object"""
        session_info["altcha_public_key"] = bool(
            self.env["ir.config_parameter"].sudo().get_param("altcha.key")
        )
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
        altcha_signature = request.params.get("altcha")
        if not altcha_signature:
            _logger.warning("Altcha token missing in request")
            raise UserError(_("Suspicious activity detected by Altcha"))
        altcha_request = json.loads(base64.b64decode(altcha_signature))
        is_valid, error = altcha.verify_solution(
            altcha_request,
            self.env["ir.config_parameter"].sudo().get_param("altcha.key"),
            True,
        )
        if not is_valid:
            _logger.warning("Altcha verification failed: %s", error)
            raise UserError(_("Suspicious activity detected by Altcha"))
        unique_id = self._get_altcha_key(altcha_request["signature"])
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
