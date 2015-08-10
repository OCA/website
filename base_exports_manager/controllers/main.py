# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Antonio Espinosa <antonioea@antiun.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
from openerp.addons.web.http import request
import operator


class Export(http.Controller):

    @http.route('/web/export/namelist', type='json', auth="user")
    def namelist(self, model, export_id):
        # TODO: namelist really has no reason to be in Python (although
        # itertools.groupby helps)
        export = request.session.model("ir.exports").read([export_id])[0]
        export_fields_list = request.session.model("ir.exports.line").read(
            export['export_fields'])
        fields_data = self.fields_info(
            model, map(operator.itemgetter('name'), export_fields_list))
        return [
            {'name': field['name'], 'label': fields_data[field['name']]}
            for field in export_fields_list
        ]
