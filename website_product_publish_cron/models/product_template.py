# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    expected_publish_date = fields.Datetime()
    expected_unpublish_date = fields.Datetime()

    def get_publish_domain(self):
        domain = [
            ("website_published", "=", False),
            ("expected_publish_date", "<=", fields.datetime.now()),
            "|",
            ("expected_unpublish_date", ">", fields.datetime.now()),
            ("expected_unpublish_date", "=", False),
        ]
        return domain

    def get_unpublish_domain(self):
        domain = [
            ("website_published", "=", True),
            ("expected_unpublish_date", "<=", fields.datetime.now()),
        ]
        return domain

    def _check_website_product_visibility(self):
        publish_domain = self.get_publish_domain()
        publish_products = self.env["product.template"].search(publish_domain)
        publish_products.write({"website_published": True})

        unpublish_domain = self.get_unpublish_domain()
        unpublish_products = self.env["product.template"].search(unpublish_domain)
        unpublish_products.write({"website_published": False})
