# Copyright 2026 MTS - Juan Arcos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleVatLabel(WebsiteSale):
    def _prepare_address_form_values(self, *args, **kwargs):
        # 1. Call the original function to load all the native values
        res = super()._prepare_address_form_values(*args, **kwargs)

        # 2. We obtain the current country from the values ​​already prepared by Odoo
        country_sudo = res.get("country")

        # 3. Modify the 'res' dictionary with the country specific
        # VAT label, if the country exists
        if country_sudo:
            res["vat_label"] = country_sudo.vat_label or request.env._("VAT")

        return res
