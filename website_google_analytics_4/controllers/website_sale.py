# Copyright 2023 Studio73 - Miguel Gandia <miguel@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):
    def order_lines_2_google_api(self, order_lines):
        ret = []
        for line in order_lines:
            product = line.product_id
            ret.append(
                {
                    "item_id": line.order_id.id,
                    "item_name": product.name or "-",
                    "sku": product.barcode or product.id,
                    "item_category": product.categ_id.name or "-",
                    "price": line.price_unit,
                    "quantity": line.product_uom_qty,
                }
            )
        return ret

    def order_2_return_dict(self, order):
        return {
            "transaction": {
                "transaction_id": order.id,
                "affiliation": order.company_id.name,
                "value": order.amount_total,
                "tax": order.amount_tax,
                "currency": order.currency_id.name,
                "items": self.order_lines_2_google_api(order.order_line),
            }
        }
