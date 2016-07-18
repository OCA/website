# -*- coding: utf-8 -*-
# © 2015-2016 Odoo S.A.
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openerp import http
from openerp.http import request
from openerp.fields import Date
from openerp.addons.website_portal.controllers.main import website_account


class WebsiteAccount(website_account):

    _items_per_page = 10

    def _prepare_portal_layout_values(self):
        """ prepare the values to render portal layout """
        partner = request.env.user.partner_id
        # get customer sales rep
        if partner.user_id:
            sales_rep = partner.user_id
        else:
            sales_rep = False
        values = {
            'sales_rep': sales_rep,
            'company': request.website.company_id,
            'user': request.env.user
        }
        return values

    def _get_archive_groups(self, model, domain=None, fields=None,
                            groupby="create_date", order="create_date desc"):
        if not model:
            return []
        if domain is None:
            domain = []
        if fields is None:
            fields = ['name', 'create_date']
        groups = []
        for group in request.env[model].read_group(
                domain, fields=fields, groupby=groupby, orderby=order):
            label = group[groupby]
            date_begin = date_end = None
            for leaf in group["__domain"]:
                if leaf[0] == groupby:
                    if leaf[1] == ">=":
                        date_begin = leaf[2]
                    elif leaf[1] == "<":
                        date_end = leaf[2]
            groups.append({
                'date_begin': Date.to_string(Date.from_string(date_begin)),
                'date_end': Date.to_string(Date.from_string(date_end)),
                'name': label,
                'item_count': group[groupby + '_count']
            })
        return groups

    @http.route(['/my', '/my/home'], type='http', auth="public", website=True)
    def account(self):
        values = self._prepare_portal_layout_values()
        return request.website.render(
            "website_portal_v10.portal_my_home", values)
