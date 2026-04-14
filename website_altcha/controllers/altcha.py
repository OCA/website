import json
import secrets
from datetime import timedelta

import altcha.v2 as altcha

from odoo import fields, http
from odoo.http import request


class AltchaController(http.Controller):
    @http.route("/altcha", type="http", auth="public", website=True)
    def generate_altcha_challenge(self):
        timeout = int(request.website.sudo().altcha_timeout or 5)
        cost = int(request.website.sudo().altcha_cost or 1_000)
        algorithm = request.website.sudo().altcha_algorithm or "PBKDF2/SHA-512"
        expires = fields.Datetime.now() + timedelta(minutes=timeout)
        key = request.website.sudo().altcha_key
        secret_key = request.website.sudo().altcha_private_key
        parameters = {
            "algorithm": algorithm,
            "cost": cost,
            "hmac_secret": key,
            "expires_at": expires,
        }
        if secret_key:
            parameters["hmac_key_secret"] = secret_key
            parameters["counter"] = secrets.randbelow(cost) + cost
        challenge = altcha.create_challenge(**parameters)
        request.env["altcha.key"].sudo().create(
            {
                "key": request.env["ir.http"]._get_altcha_key(challenge.signature),
                "expires_at": expires,
            }
        )
        return request.make_response(
            json.dumps(challenge.to_dict()),
            headers=[("Content-Type", "application/json")],
        )
