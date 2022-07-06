# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    custom_message = fields.Text(default="", translate=True)

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        pricelist=False,
        parent_combination=False,
        only_template=False,
    ):
        result = super(ProductTemplate, self)._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            pricelist=pricelist,
            parent_combination=parent_combination,
            only_template=only_template,
        )
        if result.get("product_id"):
            product = self.env["product.product"].browse(result.get("product_id"))
            if product.custom_message:
                result.update({"custom_message": product.custom_message})
            result.update({"qty_available": product.sudo().qty_available})
        return result
