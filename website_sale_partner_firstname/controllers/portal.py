# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    CustomerPortal.OPTIONAL_BILLING_FIELDS += [
        "firstname",
        "lastname",
    ]

    def details_form_validate(self, data):
        context = dict(request.env.context)
        # 'name' field cannont be updated as it would recompute fields
        # firstname and lastname. That is why it is set in context
        # that changes in field name need to be ignored.
        context.update({"name_ignore": True})
        request.env.context = context
        error, error_message = super().details_form_validate(data)
        partner = request.env.user.partner_id
        if partner.can_edit_vat():
            if "firstname" in data and not data.get("Name"):
                error["firstname"] = "error"
                error_message.append(_("Firstname is mandatory."))
            if (
                "lastname" in data
                and not data.get("lastname")
                and (
                    (data.get("fiscal_position_type") == "b2c")
                    or (
                        partner.fiscal_position_type == "b2c"
                        and not data.get("fiscal_position_type") == "b2b"
                    )
                )
            ):
                error["lastname"] = "error"
                error["fiscal_position_type"] = "error"
                error_message.append(_("Lastname is mandatory for B2C users."))
        else:
            if "firstname" in data and data.get("firstname") != partner.firstname:
                error["firstname"] = "error"
                error_message.append(
                    _(
                        "Changing Name is not allowed once document(s) have been "
                        "issued for your account. Please contact us directly for "
                        "this operation."
                    )
                )
            if "lastname" in data and data.get("lastname") != partner.lastname:
                error["lastname"] = "error"
                error_message.append(
                    _(
                        "Changing Lastname is not allowed once document(s) have "
                        "been issued for your account. Please contact us directly "
                        "for this operation."
                    )
                )
        return error, error_message
