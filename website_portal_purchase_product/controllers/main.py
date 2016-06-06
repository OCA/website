# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from contextlib import contextmanager
from werkzeug.exceptions import Forbidden
from openerp import _
from openerp.http import local_redirect, request, route
from openerp.addons.website_portal_purchase.controllers.main import (
    PortalPurchaseWebsiteAccount,
)
from openerp.addons.website_form.controllers.main import WebsiteForm
from ..exceptions import FormSaveError


class ProductPortalPurchaseWebsiteAccount(PortalPurchaseWebsiteAccount):
    def _purchase_product_domain(self, query=None):
        """Domain to find products or product templates.

        :param str query:
            Text filter applied by the user.
        """
        domain = [
            ("seller_ids.name", "child_of",
             request.env.user.commercial_partner_id.ids),
        ]
        if query:
            terms = query.split()
            if terms:
                for term in terms:
                    domain += [
                        "|",
                        ("name", "ilike", term),
                        ("description_sale", "ilike", term)
                    ]
        return domain

    def _purchase_product_update(self, product, post):
        """Update the product with the received form values.

        :param product.template product:
            Product record to update.

        :param dict post:
            Values as they came from the form.

        :return dict:
            Mapping of form::

                {
                    'field_name': {
                        'human': 'human-readable field name',
                        'errors': [
                            'Error message',
                            ...
                        ],
                    },
                    ...
                }
        """
        errors = dict()
        supplierinfo_found = dict()
        SupplierInfo = request.env["product.supplierinfo"]
        required = self._purchase_product_required_fields()

        try:
            with request.env.cr.savepoint():
                for form_field, value in post.iteritems():
                    # Select the right supplierinfo record
                    if form_field.startswith("supplierinfo_"):
                        id_, db_field = form_field.split("_", 2)[1:]
                        id_ = int(id_)
                        try:
                            record = supplierinfo_found[id_]
                        except KeyError:
                            supplierinfo_found[id_] = record = (
                                SupplierInfo.browse(id_) if id_
                                else SupplierInfo.new({
                                    "product_id": product.id,
                                    "name": (request.env.user
                                             .commercial_partner_id),
                                }))

                    # Select the product record
                    else:
                        record, db_field = product, form_field

                    # Required fields cannot be empty
                    if form_field in required:
                        required.discard(form_field)
                        if not value:
                            self._purchase_product_add_error(
                                errors, product, form_field, db_field,
                                _("Required field"))
                            continue

                    # Try to save the converted received value
                    try:
                        with request.env.cr.savepoint():
                            self._set_field(record, db_field, value)

                    # If it fails, log the error
                    except Exception as error:
                        self._purchase_product_add_error(
                            errors, record, form_field, db_field,
                            ": ".join(a or "" for a in error.args))

                # No more required fields should remain now
                for form_field in required:
                    self._purchase_product_add_error(
                        errors, product, form_field, db_field,
                        _("Required field"))

                # Rollback if there were errors
                if errors:
                    raise FormSaveError()

        # This is just to force rollback to first savepoint
        except FormSaveError:
            pass

        return errors

    def _purchase_product_required_fields(self):
        """These fields must be filled."""
        return {"name", "type", "price"}

    def _purchase_product_add_error(self, errors, record, form_field, db_field,
                                    message):
        """Save an error while processing the form.

        :param dict errors:
            Errors dict to be modified.

        :param models.Model record:
            Will extract the human-readable field name from this record.

        :param str form_field:
            Name of the field in the form that produced the error.

        :param str db_field:
            Name of the field in the :param:`record`.

        :param str message:
            Error message.

        :return dict:
            Returns the modified :param:`errors` dict.
        """
        if form_field not in errors:
            errors[form_field] = {
                "human":
                    record._fields[db_field]
                    .get_description(request.env)["string"],
                "errors": list(),
            }
        errors[form_field]["errors"].append(message)
        return errors

    def _set_field(self, record, field_name, value):
        """Set a field's value."""
        if value == "":
            value = False
        else:
            website_form = WebsiteForm()
            converter = website_form._input_filters[
                record._fields[field_name].get_description(request.env)
                ["type"]]
            value = converter(website_form, field_name, value)
        record[field_name] = value

    @route(["/my/purchase/products",
            "/my/purchase/products/page/<int:page>"],
           type='http', auth="user", website=True)
    def portal_my_purchase_products(self, page=1, date_begin=None,
                                    date_end=None, search=None, **post):
        values = self._prepare_portal_layout_values()
        url = "/my/purchase/products"
        ProductTemplate = request.env["product.template"].with_context(
            pricelist=request.website.get_current_pricelist().id)
        domain = self._purchase_product_domain(search)
        archive_groups = self._get_archive_groups(
            ProductTemplate._name, domain)
        if date_begin and date_end:
            domain += [("create_date", ">=", date_begin),
                       ("create_date", "<", date_end)]

        # Make pager
        count = ProductTemplate.search_count(domain)
        url_args = post.copy()
        url_args.update({
            "date_begin": date_begin,
            "date_end": date_end,
            "search": search,
        })
        pager = request.website.pager(
            url=url,
            url_args=url_args,
            total=count,
            page=page,
            step=self._items_per_page,
        )

        # Sarch the count to display, according to the pager data
        products = ProductTemplate.search(
            domain, limit=self._items_per_page, offset=pager["offset"])

        values.update({
            "archive_groups": archive_groups,
            "date": date_begin,
            "default_url": url,
            "pager": pager,
            "products": products,
            "search": search,
        })

        return request.website.render(
            "website_portal_purchase_product.portal_my_products", values)

    @route(
        ['/my/purchase/products/<model("product.template"):product>',
         '/my/purchase/products/new'],
        type='http', auth="user", website=True)
    def my_purchase_product_form(self, product=None, **kwargs):
        """Display a form to edit or create a product.

        :param "new"/product.template prodcut:
            Product we are editing. If the user has no access, this will
            automatically raise a ``403 Forbidden`` error.
        """
        # Only show forms for those that can edit or create their products
        if product:
            product.check_access_rule("write")
        else:
            product = request.env["product.template"]
            product.check_access_rights("create")

        # Prepare form
        values = self._prepare_portal_layout_values()
        values["product"] = (
            product or product.new()).with_context(
                pricelist=request.website.get_current_pricelist().id)

        values["errors"] = (self._purchase_product_update(product, kwargs)
                            if kwargs else dict())
        return request.website.render(
            "website_portal_purchase_product.products_followup", values)

    @route(
        ["/my/purchase/products/<model('product.template'):product>/disable"],
        type="http", auth="user", website=True)
    def my_purchase_product_disable(self, product,
                                    redirect="/my/purchase/products"):
        """This product will disappear from the supplier's panel.

        They will think it was deleted, but it was just disabled.
        """
        product.website_published = product.active = False
        return local_redirect(redirect, kwargs)

    @route()
    def account(self):
        """Display product count in account summary for suppliers."""
        response = super(ProductPortalPurchaseWebsiteAccount, self).account()
        if "supplier_order_count" in response.qcontext:
            response.qcontext["supplier_product_count"] = (
                request.env['product.template']
                .search_count(self._purchase_product_domain()))
        return response
