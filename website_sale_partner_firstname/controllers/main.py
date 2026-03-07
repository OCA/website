from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalFirstLastName(CustomerPortal):
    """Replace 'name' with firstname/lastname on checkout and portal."""

    def _create_or_update_address(self, partner_sudo, **form_data):
        """Synthesize 'name' from firstname/lastname so the base code's
        address_values['name'] check doesn't raise a KeyError."""
        if "name" not in form_data and (
            "firstname" in form_data or "lastname" in form_data
        ):
            firstname = (form_data.get("firstname") or "").strip()
            lastname = (form_data.get("lastname") or "").strip()
            form_data["name"] = request.env["res.partner"]._get_computed_name(
                lastname,
                firstname,
            )
        return super()._create_or_update_address(partner_sudo, **form_data)

    def _get_mandatory_billing_address_fields(self, country_sudo):
        """Swap 'name' for 'firstname' and 'lastname' in mandatory billing fields."""
        fields = super()._get_mandatory_billing_address_fields(country_sudo)
        fields.discard("name")
        fields |= {"firstname", "lastname"}
        return fields

    def _get_mandatory_delivery_address_fields(self, country_sudo):
        """Swap 'name' for 'firstname' and 'lastname' in mandatory delivery fields."""
        fields = super()._get_mandatory_delivery_address_fields(country_sudo)
        fields.discard("name")
        fields |= {"firstname", "lastname"}
        return fields

    def portal_address_country_info(self, country, address_type, **kw):
        """Update the JS required-fields list for firstname/lastname."""
        result = super().portal_address_country_info(country, address_type, **kw)
        if "required_fields" in result:
            result["required_fields"] = [
                f for f in result["required_fields"] if f != "name"
            ]
            for field in ("firstname", "lastname"):
                if field not in result["required_fields"]:
                    result["required_fields"].append(field)
        return result
