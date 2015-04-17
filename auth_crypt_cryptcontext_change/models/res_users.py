# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
#                 Antonio Espinosa <antonioea@antiun.com>
#                 Javier Iniesta <javieria@antiun.com>
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
from passlib.context import CryptContext
from passlib.hash import bcrypt

import logging
from pprint import pformat
_logger = logging.getLogger(__name__)


class resUsers(models.Model):
    _inherit = "res.users"

    def _crypt_context(self, cr, uid, id, context=None):
        uid = super(resUsers, self)._crypt_context(
            cr, uid, id, context=context)

        default_crypt_context = CryptContext(
            ['pbkdf2_sha512', 'md5_crypt', 'bcrypt'],
            deprecated=['md5_crypt', 'bcrypt'],
        )
        return default_crypt_context
