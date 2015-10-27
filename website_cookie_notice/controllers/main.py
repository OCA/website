# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#    Copyright (C) 2015 Antiun Ingeniería S.L. <http://antiun.com>
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

from openerp import http


class CookieNotice(http.Controller):
    @http.route("/website_cookie_notice/ok", auth="public")
    def accept_cookies(self):
        """Stop spamming with cookie banner."""
        http.request.httpsession["accepted_cookies"] = True
        return http.local_redirect("/")
