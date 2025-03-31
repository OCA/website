# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_alternative_price(
        self, pricelist, partner, product_id, fiscal_position, company, qty=1.0
    ):
        product = self.env["product.template"].browse(product_id)
        product_taxes = product.sudo().taxes_id.filtered(
            lambda t: t.company_id == company
        )
        taxes = fiscal_position.map_tax(product_taxes)
        alternative_price = pricelist._get_product_price(product, qty)
        return self._price_with_tax_computed(
            alternative_price,
            product_taxes,
            taxes,
            self.env.company.id,
            pricelist,
            product,
            partner,
        )

    def _get_sales_prices(self, pricelist):
        if (
            pricelist
            and pricelist.discount_policy == "without_discount"
            and self.env.context.get("website_id")
        ):
            pricelist = pricelist.with_context(skip_alternative_pricelist=True)
            res = super()._get_sales_prices(pricelist)
            partner = self.env.user.partner_id
            fpos_id = self.env["website"]._get_current_fiscal_position_id(partner)
            fiscal_position = self.env["account.fiscal.position"].sudo().browse(fpos_id)
            pricelist = pricelist.with_context(skip_alternative_pricelist=False)
            current_website = self.env["website"].get_current_website()
            company = current_website.company_id
            for product_id in res:
                res[product_id]["base_price"] = res[product_id]["price_reduce"]
                res[product_id]["price_reduce"] = self._get_alternative_price(
                    pricelist, partner, product_id, fiscal_position, company
                )
            return res
        return super()._get_sales_prices(pricelist)

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        pricelist=False,
        parent_combination=False,
        only_template=False,
    ):
        if (
            pricelist
            and pricelist.discount_policy == "without_discount"
            and self.env.context.get("website_id")
        ):
            # Compute original price
            pricelist = pricelist.with_context(skip_alternative_pricelist=True)
            combination_info = super(ProductTemplate, self)._get_combination_info(
                combination,
                product_id,
                add_qty,
                pricelist,
                parent_combination,
                only_template,
            )
            combination_info["list_price"] = combination_info["price"]
            combination_info["base_price"] = combination_info["price"]
            # Compute alternative price
            pricelist = pricelist.with_context(skip_alternative_pricelist=False)
            product = self.env["product.product"].browse(combination_info["product_id"])
            current_website = self.env["website"].get_current_website()
            company = current_website.company_id
            partner = self.env.user.partner_id
            fpos_id = (
                self.env["website"].sudo()._get_current_fiscal_position_id(partner)
            )
            fiscal_position = self.env["account.fiscal.position"].sudo().browse(fpos_id)
            combination_info["price"] = self._get_alternative_price(
                pricelist,
                partner,
                product.product_tmpl_id.id,
                fiscal_position,
                company,
                self.env.context.get("quantity", add_qty),
            )
            combination_info["has_discounted_price"] = (
                pricelist.currency_id.compare_amounts(
                    combination_info["list_price"], combination_info["price"]
                )
                == 1
            )
            return combination_info
        return super()._get_combination_info(
            combination,
            product_id,
            add_qty,
            pricelist,
            parent_combination,
            only_template,
        )
