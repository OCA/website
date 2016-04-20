# -*- coding: utf-8 -*-
# Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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
    'cookieAcceptButtonText',
    'cookieDeclineButtonText',
    'cookieResetButtonText',
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
