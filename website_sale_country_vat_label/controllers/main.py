# Copyright 2026 MTS - Juan Arcos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleVatLabel(WebsiteSale):
    def _prepare_address_form_values(self, *args, **kwargs):
        """Extend standard address values to support country-specific VAT labels.

        This method overrides the generic 'VAT' label by checking if the
        currently selected country has a custom label configured (e.g., RUT,
        CPF). If found, it replaces the default label to improve localization.
        """
        res = super()._prepare_address_form_values(*args, **kwargs)
        country_sudo = res.get("country")

        if country_sudo:
            res["vat_label"] = country_sudo.vat_label or request.env._("VAT")

        return res
