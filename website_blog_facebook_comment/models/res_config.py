# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
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

from openerp import models, fields, api


class DigitalConfigSettings(models.TransientModel):
    _name = 'website.blog.facebook.comment.settings'
    _inherit = 'res.config.settings'

    appId = fields.Char(string="Facebook AppID")
    numposts = fields.Char(string="Number of Posts", default=5)

    @api.multi
    def get_default_appid(self):
        conf_par = self.env['ir.config_parameter']
        token = conf_par.get_param('blog_facebook_comment.appId', default="")
        return {'token': token}

    @api.multi
    def set_appid(self):
        conf_par = self.env['ir.config_parameter']
        conf_par.set_param('blog_facebook_comment.appId', self.appId)

    @api.multi
    def get_default_numposts(self):
        conf_par = self.env['ir.config_parameter']
        token = conf_par.get_param('blog_facebook_comment.numposts', default="")
        return {'token': token}

    @api.multi
    def set_numposts(self):
        conf_par = self.env['ir.config_parameter']
        if self.numposts <= 0:
            self.numposts = 5
        conf_par.set_param('blog_facebook_comment.numposts', self.numposts)
