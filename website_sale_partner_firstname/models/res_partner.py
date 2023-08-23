# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo import api, models
from odoo.http import request


class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def signup_retrieve_info(self, token):
        res = super().signup_retrieve_info(token)
        partner = self._signup_retrieve_partner(token, raise_exception=True)
        res.update(
            {
                "name": partner.firstname,
                "lastname": partner.lastname,
            }
        )
        return res

    def write(self, vals):
        if vals.get("name") and request.env.context.get("name_ignore"):
            vals.pop("name")
        return super().write(vals)
