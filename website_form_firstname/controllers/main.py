# -*- coding: utf-8 -*-
# Copyright 2018 Denis Mudarisov (IT-Projects LLC)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleExtended(WebsiteSale):
    def _get_mandatory_billing_fields(self):
        fields = super()._get_mandatory_billing_fields()
        fields = list(filter(lambda x: x != "name", fields))
        return fields

    def _get_mandatory_shipping_fields(self):
        fields = super()._get_mandatory_shipping_fields()
        fields = list(filter(lambda x: x != "name", fields))
        return fields
