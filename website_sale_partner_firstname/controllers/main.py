# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo.http import request

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _get_mandatory_fields_shipping(self, country_id=False):
        req = super()._get_mandatory_fields_shipping(country_id)
        req += ["firstname"]
        if "name" in req:
            req.remove("name")
        return req

    def _get_mandatory_fields_billing(self, country_id=False):
        req = super()._get_mandatory_fields_billing(country_id)
        req.append("firstname")
        if request.env.context.get("fiscal_position_type") == "b2c":
            req.append("lastname")
        # Name is removed as this field cannot be explicitly edited
        # It is edited in the backend through the fields first name
        # and lastname
        if "name" in req:
            req.remove("name")
        return req

    def values_postprocess(self, order, mode, values, errors, error_msg):
        new_values, errors, error_msg = super(WebsiteSale, self).values_postprocess(
            order=order, mode=mode, values=values, errors=errors, error_msg=error_msg
        )
        new_values.update(
            {
                "firstname": values.get("firstname") or "",
                "lastname": values.get("lastname") or "",
            }
        )
        # Name is removed as this field cannot be explicitly edited
        # It is edited in the backend through the fields first name
        # and lastname
        new_values.pop("name")
        return new_values, errors, error_msg

    def checkout_form_validate(self, mode, all_form_values, data):
        required_fields = [
            f for f in (all_form_values.get("field_required") or "").split(",") if f
        ]
        # Name is removed as this field cannot be explicitly edited
        # It is edited in the backend through the fields first name
        # and lastname
        if "name" in required_fields:
            required_fields.remove("name")
        all_form_values["field_required"] = ",".join(required_fields)
        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data
        )
        if data.get("partner_id"):
            partner_su = (
                request.env["res.partner"]
                .sudo()
                .browse(int(data["partner_id"]))
                .exists()
            )
            can_edit_vat = (
                partner_su.parent_id.can_edit_vat()
                if partner_su.parent_id
                else partner_su.can_edit_vat()
            )
            firstname_change = (
                partner_su
                and "firstname" in data
                and data["firstname"] != partner_su.firstname
            )
            if firstname_change and not can_edit_vat:
                error["firstname"] = "error"
                error_message.append(
                    _(
                        "Changing your name is not allowed once invoices have been"
                        " issued for your account. Please contact us directly for "
                        "this operation."
                    )
                )
            # When lastname field in form is empty, its values is False
            # When lastname field in backend is empty, its values is ''
            # In that case, if both are compared, they are considered to be
            # different so data['lastname'] != partner_su.lastname would
            # return True although no real change would have been applied.
            lastname_change = (
                partner_su
                and "lastname" in data
                and data["lastname"] != partner_su.lastname
                and (data["lastname"] or partner_su.lastname not in ["", False])
            )
            if lastname_change and not can_edit_vat:
                error["lastname"] = "error"
                error_message.append(
                    _(
                        "Changing your last name is not allowed once invoices have"
                        " been issued for your account. Please contact us directly"
                        " for this operation."
                    )
                )

            # Prevent change the partner name, lastname if
            # it is an internal user.
            if (firstname_change or lastname_change) and not all(
                partner_su.user_ids.mapped("share")
            ):
                error.update(
                    {
                        "firstname": "error" if firstname_change else None,
                        "lastname": "error" if lastname_change else None,
                    }
                )
                error_message.append(
                    _(
                        "If you are ordering for an external person, please place "
                        "your order via the backend. If you wish to change your "
                        "name or last name, please do so in the account settings "
                        "or contact your administrator."
                    )
                )
        return error, error_message


class AuthSignupHome(AuthSignupHome):
    def get_auth_signup_qcontext(self):
        qcontext = super().get_auth_signup_qcontext()
        qcontext.update(
            {
                k: v
                for (k, v) in request.params.items()
                if k
                in {
                    "lastname",
                }
            }
        )
        if "name" in qcontext:
            qcontext["firstname"] = qcontext["name"]
        if (
            "error" not in qcontext
            and request.httprequest.method == "POST"
            and qcontext.get("fiscal_position_type") == "b2c"
            and not qcontext.get("lastname")
        ):
            qcontext["error"] = _("Lastname is required for B2C users.")
        return qcontext

    def _prepare_signup_values(self, qcontext):
        values = super()._prepare_signup_values(qcontext)
        if "firstname" in qcontext:
            values["firstname"] = qcontext["firstname"]
        if "lastname" in qcontext:
            values["lastname"] = qcontext["lastname"]
        return values
