# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import base64

from openerp import http
from openerp.http import request

from openerp.addons.website_portal.controllers.main import WebsiteAccount


PPG = 10  # Products Per Page


class WebsiteProductSupplier(http.Controller):

    mandatory_product_fields = ['product_name']
    optional_product_fields = ['product_code', 'min_qty', 'delay']

    def _get_mandatory_product_fields(self):
        return self.mandatory_product_fields

    def _get_optional_product_fields(self):
        return self.optional_product_fields

    def check_product_form_validate(self, data):
        error = dict()
        for field_name in self._get_mandatory_product_fields():
            if not data.get(field_name):
                error[field_name] = 'missing'
        return error

    def _post_prepare_supplierinfo_query(self, supplierinfo_dic, data):
        return supplierinfo_dic

    def supplierinfo_field_parse(self, data):
        # set mandatory and optional fields
        all_fields = (
            self._get_mandatory_product_fields() +
            self._get_optional_product_fields())
        # set data
        if isinstance(data, dict):
            supplierinfo_dic = dict(
                (field_name, data[field_name]) for field_name in
                all_fields if field_name in data)
        else:
            supplierinfo_dic = dict(
                (field_name, getattr(data, field_name)) for field_name in
                all_fields)
        supplierinfo_dic = self._post_prepare_supplierinfo_query(
            supplierinfo_dic, data)
        return supplierinfo_dic

    @http.route([
        '/my/supplier/product/<model("product.supplierinfo"):supplierinfo>',
        '/my/supplier/product/new'
    ], type='http', auth="user", website=True)
    def supplier_info(self, supplierinfo=None, category='', search='', **post):
        if supplierinfo and supplierinfo.name != request.env.user.partner_id:
            return request.website.render('website.404')

        values = {
            'search': search,
            'category': category,
            'error': {},
            'user': request.env.user,
        }
        if supplierinfo is None:
            supplierinfo = request.env['product.supplierinfo']
        supplierinfo = supplierinfo.sudo()
        form_vals = self.supplierinfo_field_parse(supplierinfo)
        values.update(self._prepare_render_values(supplierinfo, form_vals))
        return request.website.render(
            "website_product_supplier.product", values)

    def _prepare_render_values(self, supplierinfo, form_vals):
        values = {
            'main_obj': supplierinfo,
            'supplierinfo': form_vals,
            'product': supplierinfo.product_tmpl_id,
            'user': request.env.user,
            'pricelist': supplierinfo.pricelist_ids,
        }
        return values

    @http.route('/my/supplier/product/save/', type='http', auth="user",
                website=True)
    def supplier_info_create(self, **post):
        supplierinfo = request.env['product.supplierinfo'].sudo()
        form_vals = self.supplierinfo_field_parse(post)
        values = self._prepare_render_values(supplierinfo, form_vals)
        values['error'] = self.check_product_form_validate(form_vals)
        if values["error"]:
            return request.website.render(
                "website_product_supplier.product",
                values)

        product_vals = {'name': form_vals.get('product_name')}
        if post.get('ufile', False):
            product_vals.update(
                image=base64.encodestring(post['ufile'].read()))
        product = supplierinfo.product_tmpl_id.create(
            self._prepare_product_values(product_vals))
        form_vals.update({
            'name': request.env.user.partner_id.id,
            'product_tmpl_id': product.id,
            'pricelist_ids': [(0, 0, {
                'min_quantity': post.get('min_quantity', 0.0),
                'price': post.get('price', 0.0)})]
        })
        values['product'] = product
        try:
            supplierinfo = supplierinfo.create(
                self._prepare_supplierinfo_values(
                    supplierinfo, product, form_vals, post))
            values.update({
                'product': product,
                'main_obj': supplierinfo,
                'pricelist': supplierinfo.pricelist_ids
            })
        except:
            values.update(error={'error_name': 'Invalid fields'})
            return request.website.render(
                "website_product_supplier.product",
                values)
        return http.redirect_with_hash(
            '/my/supplier/product/%s' % supplierinfo.id)

    @http.route('/my/supplier/product/save/<model("product.supplierinfo"):supp'
                'lierinfo>', type='http', auth="user", website=True)
    def supplier_info_save(self, supplierinfo=None, **post):
        if supplierinfo.name != request.env.user.partner_id:
            return request.website.render('website.404')
        supplierinfo = supplierinfo.sudo()
        form_vals = self.supplierinfo_field_parse(post)
        values = self._prepare_render_values(supplierinfo, form_vals)
        values['error'] = self.check_product_form_validate(form_vals)
        if values["error"]:
            return request.website.render(
                "website_product_supplier.product",
                values)
        try:
            form_vals.update({
                'pricelist_ids': [(1, supplierinfo.pricelist_ids[0].id, {
                    'min_quantity': post.get('min_quantity', 0.0),
                    'price': post.get('price', 0.0)})]})
            supplierinfo.write(self._prepare_supplierinfo_values(
                supplierinfo, supplierinfo.product_tmpl_id, form_vals, post))
        except:
            values.update(error={'error_name': 'Invalid fields'})
            return request.website.render(
                "website_product_supplier.product",
                values)
        return http.redirect_with_hash(
            '/my/supplier/product/%s' % supplierinfo.id)

    def _prepare_supplierinfo_values(self, supplierinfo, product, vals, post):
        # Hook to rewrite
        return vals

    def _prepare_product_values(self, vals):
        # Hook to rewrite
        return vals

    def _prepare_supplierinfo_list(self, supplierinfo, pager):
        values = {
            'suppliersinfo': supplierinfo,
            'pager': pager,
            'user': request.env.user,
        }
        return values

    def _get_search_domain(self, search=None):
        domain = [('name', '=', request.env.user.partner_id.id)]
        if search:
            for srch in search.split(" "):
                domain += [
                    ('product_name', 'ilike', srch),
                ]
        return domain

    @http.route(['/my/supplier/product/list',
                 '/my/supplier/product/list/page/<int:page>'],
                type='http', auth="user", website=True)
    def supplierinfo_list(self, page=0, **post):
        supplierinfo_obj = request.env['product.supplierinfo']
        domain = self._get_search_domain(post.get('search', ''))
        url = "/my/supplier/product/list_only"
        supplierinfo_count = supplierinfo_obj.search_count(domain)

        pager = request.website.pager(
            url=url, total=supplierinfo_count, page=page, step=PPG, scope=7,
            url_args=post)
        supplierinfo = supplierinfo_obj.search(
            domain, limit=PPG, offset=pager['offset'])

        values = self._prepare_supplierinfo_list(supplierinfo, pager)

        return request.website.render(
            "website_product_supplier.product", values)

    @http.route(['/my/supplier/product/list_only',
                 '/my/supplier/product/list_only/page/<int:page>'],
                type='http', auth="user", website=True)
    def supplier_product_list(self, page=0, **post):
        res = self.supplierinfo_list(page, **post)
        res.template = "website_product_supplier.supplier_product_list"
        return res

    @http.route(['/my/supplier/product/delete'], type='json',
                auth="user", website=True)
    def delete_product(self, supplierinfo_id):
        supplierinfo = request.env['product.supplierinfo'].browse(
            int(supplierinfo_id))
        if len(supplierinfo.product_tmpl_id.seller_ids) == 1:
            res = supplierinfo.product_tmpl_id.unlink()
        else:
            res = supplierinfo.unlink()
        return res


class ProductSupplierWebsiteAccount(WebsiteAccount):

    @http.route(['/my/home'], type='http', auth="user", website=True)
    def account(self, **kw):
        response = super(ProductSupplierWebsiteAccount, self).account(**kw)
        if not request.env.user.partner_id.supplier:
            return response
        supplierinfo_obj = request.env['product.supplierinfo']
        domain = [('name', '=', request.env.user.partner_id.id)]
        supplierinfo = supplierinfo_obj.search(domain, limit=PPG)
        values = {
            'suppliersinfo': supplierinfo,
            'pager': False,
            'user': request.env.user,
        }
        response.qcontext.update(values)
        return response
