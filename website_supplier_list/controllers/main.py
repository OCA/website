# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.addons.web import http
from openerp.tools.translate import _
from openerp.addons.web.http import request
import werkzeug.urls


class WebsiteSupplier(http.Controller):
    _references_per_page = 20

    def _get_country_ids(self, country_id, country_ids):
        country_obj = request.env['res.country']

        if not any(
            x['country_id'][0] == country_id
                for x in country_ids if x['country_id']):
            country = country_obj.read(
                country_id, ['name'])
            if country:
                country_ids.append({
                    'country_id_count': 0,
                    'country_id': (country_id, country['name'])
                })
            country_ids.sort(
                key=lambda d: d['country_id'] and d['country_id'][1])

        return country_ids

    @http.route([
        '/suppliers',
        '/suppliers/page/<int:page>',
        '/suppliers/country/<model("res.country"):countries>',
        '/suppliers/country/<model("res.country"):countries>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def suppliers(self, countries=None, page=0, **post):
        partner_obj = request.env['res.partner']
        partner_name = post.get('search', '')
        url = '/suppliers'
        country_ids = []
        country_id = False

        domain = [
            ('website_supplier_published', '=', True),
            ('supplier', '=', True)
        ]
        if partner_name:
            domain += [
                '|',
                ('name', 'ilike', post.get("search")),
                ('website_description', 'ilike', post.get("search"))
            ]

        country_ids = partner_obj.read_group(
            domain, ["id", "country_id"],
            groupby="country_id", orderby="country_id")
        country_count = partner_obj.search_count(domain)

        if countries:
            country_id = countries.id
            if country_id:
                country_ids = self._get_country_ids(country_id, country_ids)
                url += '/country/%s' % (country_id)
                domain += [('country_id', '=', country_id)]

        country_ids.insert(0, {
            'country_id_count': country_count,
            'country_id': (0, _("All Countries"))
        })

        partner_count = partner_obj.search_count(domain)

        pager = request.website.pager(
            url=url, total=partner_count, page=page,
            step=self._references_per_page,
            scope=7, url_args=post
        )

        partner_ids = partner_obj.search(
            domain, offset=pager['offset'],
            limit=self._references_per_page)

        values = {
            'countries': country_ids,
            'current_country_id': country_id or 0,
            'partners': partner_ids,
            'pager': pager,
            'post': post,
            'search_path': "?%s" % werkzeug.url_encode(post),
        }
        return request.website.render("website_supplier_list.index", values)

    @http.route(
        ['/suppliers/<int:partner_id>'],
        type='http',
        auth="public",
        website=True)
    def partners_detail(self, partner_id, **post):
        obj_partner = request.env['res.partner']
        if partner_id:
            partner = obj_partner.browse(partner_id)
            if partner.exists() and partner.website_published:
                values = {}
                values['main_object'] = values['partner'] = partner
                return request.website.render(
                    "website_supplier_list.details", values)
        return self.suppliers(**post)
