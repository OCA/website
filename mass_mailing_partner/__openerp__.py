# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#    Copyright (c) 2015 Antiun Ingeniería S.L.
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
{
    "name": "Link partners with mass-mailing",
    "version": "1.0",
    "author": "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Antiun Ingeniería S.L.",
    "license": "AGPL-3",
    "category": "Marketing",
    "depends": [
        'mass_mailing',
    ],
    "post_init_hook": "_match_existing_contacts",
    'data': [
        'views/mail_mass_mailing_contact_view.xml',
        'views/mail_mass_mailing_view.xml',
        'views/res_partner_view.xml',
    ],
    "installable": True,
}
