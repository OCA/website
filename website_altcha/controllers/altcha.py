import json
from datetime import timedelta

import altcha.v1 as altcha

from odoo import fields, http
from odoo.http import request


class AltchaController(http.Controller):
    @http.route("/altcha", type="http", auth="public")
    def generate_altcha_challenge(self):
        expires = fields.Datetime.now() + timedelta(minutes=5)
        # TODO: Set the time dynamically based on config
        options = altcha.ChallengeOptions(
            hmac_key=request.env["ir.config_parameter"].sudo().get_param("altcha.key"),
            expires=expires,
        )
        challenge = altcha.create_challenge(options)
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
