# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def signup(self, values, token=None):
        if token:
            partner = self.env["res.partner"]._signup_retrieve_partner(
                token, check_validity=True, raise_exception=True
            )
            partner_user = partner.user_ids and partner.user_ids[0] or False
            # Don't update firstname and lastname if partner
            # related to user exists (i.e. when resetting password)
            if partner_user:
                values.pop("firstname", None)
                values.pop("lastname", None)
        return super().signup(values, token)

    def _create_user_from_template(self, values):
        user = super()._create_user_from_template(values)
        # Because of the way the name is computed, it is important to
        # reset the values so the final name is correct.
        # It cannot be done before (the way would be setting the value of name
        # if param. values to '') as the funcion _create_user_from_template
        # checks that values contains a value for 'name'
        user.write(
            {
                "firstname": values.get("firstname"),
                "lastname": values.get("lastname"),
            }
        )
        return user
