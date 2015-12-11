# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2015 OpenERP S.A. (<http://www.odoo.com>).
#    Copyright (c) 2015 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Collapsible product categories in website shop',
    'version': '8.0.1.0.0',
    'category': 'Sales Management',
    'author': 'OpenERP SA, '
              'Serv. Tecnol. Avanzados - Pedro M. Baeza, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.serviciosbaeza.com',
    'depends': [
        'website_sale',
    ],
    'data': [
        'views/website_sale_template.xml',
    ],
    "installable": True,
}
