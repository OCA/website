# -*- coding: utf-8 -*-
#
#    © 2015 Agile Business Group (<http://www.agilebg.com>)
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#    See __openerp__.py file
#

import logging
from openerp.addons.website.controllers.main import Website
from openerp.addons.web import http
from openerp.http import request

_logger = logging.getLogger(__name__)
try:
    from ipwhois import IPWhois
    from ipwhois import IPDefinedError
except ImportError:
    _logger.debug("Can not 'import ipwhois'.")


class LocalizedPages(Website):

    def get_country_by_ip(self, ip_addr):
        try:
            whois_info = IPWhois(ip_addr)
        except IPDefinedError:
            return None
        results = whois_info.lookup(False)
        country = request.env['res.country'].search(
            [('code', '=', results['nets'][0]['country'])])
        return country

    @http.route()
    def page(self, page, **opt):
        view = request.website.get_template(page)
        if request.httprequest.remote_addr and view.country_line_ids:
            country = self.get_country_by_ip(request.httprequest.remote_addr)
            if country:
                country_view = view.country_line_ids.filtered(
                    lambda x: x.country == country)[:1]
                page = country_view.localized_view_id.xml_id or page
        return super(LocalizedPages, self).page(page, **opt)
