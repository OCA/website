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

from openerp import tools
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time


class res_partner(osv.osv):
    _inherit = "res.partner"
    _columns = {
        'facebook_url': fields.char('Facebook'),
        'twitter_url': fields.char('Twitter'),
        'youtube_url': fields.char('Youtube'),
        'instagram_url': fields.char('instagram'),
        'googleplus_url': fields.char('Google+'),
    }

    _defaults = {
    }





