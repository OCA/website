# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from urllib.parse import unquote

from odoo import models
from odoo.http import request

CONSENT_COOKIE = "cookiefirst-consent"


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _is_allowed_cookie(cls, cookie_type):
        result = super()._is_allowed_cookie(cookie_type)
        if not result or cookie_type != "optional":
            return result
        if not request.env["website"].get_current_website().cookiefirst_identifier:
            return result
        try:
            consent = json.loads(unquote(request.cookies.get(CONSENT_COOKIE, "")))
        except ValueError:
            return False
        return isinstance(consent, dict) and consent.get("performance") is True
