# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.addons.web import http
from openerp.http import request

CONFIG_FIELDS = [
    'cookieAnalytics',
    'cookieMessage',
    'cookiePolicyLink',
    'cookieOverlayEnabled',
    'cookieAnalyticsMessage',
    'cookieErrorMessage',
    'cookieDeclineButton',
    'cookieAcceptButton',
    'cookieResetButton',
    'cookieWhatAreTheyLink',
    ]


class CookieNotice(http.Controller):
    @http.route(
        ['/cookie_notice/get_config'], type='json', auth="public",
        website=True)
    def get_cookie_notice_config(self):
        cr, uid, context, pool = (
            request.cr, request.uid, request.context, request.registry)
        user_model = pool['res.users']
        company_model = pool['res.company']
        company_id = user_model._get_company(cr, uid, context)
        company = company_model.browse(cr, uid, company_id, context)
        res = {}
        for field in CONFIG_FIELDS:
            res[field] = getattr(company, field)
        return res
