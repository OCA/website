from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleFirstLastName(WebsiteSale):
    """Replace the single 'name' field with firstname/lastname on checkout and portal."""

    # -------------------------------------------------------------------------
    # Shared (affects both checkout and portal)
    # -------------------------------------------------------------------------

    def _get_mandatory_fields(self):
        """Swap 'name' for 'firstname' and 'lastname' in mandatory fields."""
        mandatory_fields = super()._get_mandatory_fields()
        if 'name' in mandatory_fields:
            mandatory_fields.remove('name')
        mandatory_fields.extend(['firstname', 'lastname'])
        return mandatory_fields

    # -------------------------------------------------------------------------
    # Portal /my/account
    # -------------------------------------------------------------------------

    def details_form_validate(self, data, *args, **kwargs):
        """Strip whitespace from name fields so blank strings fail validation."""
        for field in ('firstname', 'lastname'):
            if field in data and isinstance(data[field], str):
                data[field] = data[field].strip()
        return super().details_form_validate(data, *args, **kwargs)

    def on_account_update(self, values, partner):
        """Ensure 'name' is present to prevent KeyError in bank-holder check."""
        result = super().on_account_update(values, partner)
        # With partner_firstname, name is computed from firstname/lastname,
        # so set the current name to prevent KeyError.
        if 'name' not in values:
            values['name'] = partner.name or ''
        return result

    # -------------------------------------------------------------------------
    # Checkout /shop/address
    # -------------------------------------------------------------------------

    def _get_mandatory_address_fields(self, country_sudo):
        """Swap 'name' for 'firstname' and 'lastname' in mandatory address fields."""
        mandatory_fields = super()._get_mandatory_address_fields(country_sudo)
        mandatory_fields.discard('name')
        mandatory_fields |= {'firstname', 'lastname'}
        return mandatory_fields

    def shop_country_info(self, country, address_type, **kw):
        """Update the JS required-fields list for firstname/lastname."""
        result = super().shop_country_info(country, address_type, **kw)
        if 'required_fields' in result:
            result['required_fields'] = [
                f for f in result['required_fields'] if f != 'name'
            ]
            for field in ('firstname', 'lastname'):
                if field not in result['required_fields']:
                    result['required_fields'].append(field)
        return result
