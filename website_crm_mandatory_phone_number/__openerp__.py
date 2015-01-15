# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2010 - 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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
    'name': 'Website CRM Contact Mandatory Phone Number',
    'version': '0.1',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'Website',
    'summary': 'This module set as required the phone number.',
    'description': """
Website CRM Contact Mandatory Phone Number
==========================================
This module set as required the phone number in the form of the
"Contact Us" page.

8th September 2014: As the way website_crm controller is build, there is no
easy way to set a field as required in the controller. Because of that,
the method had to be copied, breaking the link with any update that would be
done on this part of code.

For now, instead of overcharging the field in the controller, the field is set
as required in the view. It is weak as the behaviour won't be the same if the
field is called from another view.

Contributors
------------

* Jordi RIERA (jordi.riera@savoirfairelinux.com)
* William BEVERLY (william.beverly@savoirfairelinux.com)
* Bruno JOLIVEAU (bruno.joliveau@savoirfairelinux.com)

More informations
-----------------

Module developed and tested with Odoo version 8.0
For questions, please contact our support services (support@savoirfairelinux.com)

""",
    'depends': [
        'website_crm',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'views/website_crm.xml',
    ],
    'installable': True,
}
