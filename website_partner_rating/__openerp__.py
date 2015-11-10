# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': 'Website Partner Rating',
    'category': 'Website',
    'summary': 'Website Partner Rating',
    'website': 'www.browseinfo.in',
    'version': '1.0',
    'description': """
        You can see reviews details with Reviewer name, Rating, Date, Short & Long Description.User can submit their review only when 
    they are logged in. If the user is not logged in, then the system will provide link to login page and once after login user will
    straight away redirected to the partner page.
        You can publish/unpublish reviews from front end website page. For that you must be logged in as Administrator.
        You will able to see Avg. Rating and No. of reviews link at the top of partner detail page in website. By clicking on that you will redirect to reviews list.

        """,
    'author': 'BrowseInfo',
    'depends': ['website','website_crm_partner_assign','website_partner'],
    'installable': True,
    'data': [
        'views/template.xml',
        'views/mail_message_view.xml',
        'views/partner_rating_view.xml',
    ],
    'application': True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
