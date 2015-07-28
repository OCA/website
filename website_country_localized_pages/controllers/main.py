# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Agile Business Group (<http://www.agilebg.com>)
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

from openerp.addons.website.controllers.main import Website
from openerp.addons.web import http
from openerp.http import request
from ipwhois import IPWhois
from ipwhois import IPDefinedError


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
                for country_line in view.country_line_ids:
                    if country_line.country_id.id == country.id:
                        if country_line.localized_view_id.xml_id:
                            page = country_line.localized_view_id.xml_id
        return super(LocalizedPages, self).page(page, **opt)
