# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from contextlib import contextmanager
from openerp.http import request
from openerp.addons.website_portal_purchase_product.controllers.main import (
    ProductPortalPurchaseWebsiteAccount,
)


class PackagingPurchaseWebsiteAccount(ProductPortalPurchaseWebsiteAccount):
    def _set_field(self, record, field_name, value):
        """Handle packaging saving.

        We use a handmade cache in the session context to avoid recreating
        when setting several values for the same ``.new()`` object.
        """
        if field_name.startswith("packaging_"):
            request.context.setdefault("packagings_cached", dict())
            id_, field_name = field_name.split("_", 2)[1:]
            try:
                record = request.context["packagings_cached"][id_]
            except KeyError:
                Packaging = request.env["product.packaging"]
                record = request.context["packagings_cached"][id_] = (
                    Packaging.create({
                        "product_tmpl_id": record.id,
                        "name": record.name,
                    })
                    if id_.startswith("new")
                    else Packaging.browse(int(id_)))

        return super(PackagingPurchaseWebsiteAccount, self)._set_field(
            record, field_name, value)

    def _purchase_product_add_error(self, errors, record, form_field, db_field,
                                    message):
        """Handle packaging errors."""
        if form_field.startswith("packaging_"):
            id_, db_field = form_field.split("_", 2)[1:]
            try:
                record = request.context["packagings_cached"][id_]
            except KeyError:
                record = request.env["product.packaging"]
        return (super(PackagingPurchaseWebsiteAccount, self)
                ._purchase_product_add_error(
                    errors, record, form_field, db_field, message))

    def _purchase_product_update(self, product, post):
        """Drop removed packagings."""
        result = (super(PackagingPurchaseWebsiteAccount, self)
                  ._purchase_product_update(product, post))
        (product.packaging_ids.filtered(
            lambda r: r not in request.context["packagings_cached"].values())
            .unlink())
        return result
