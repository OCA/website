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

from openerp import models, tools, SUPERUSER_ID


class MailNotification(models.Model):
    _inherit = 'mail.notification'

    def get_signature_footer(self, cr, uid, user_id, res_model=None,
                             res_id=None, context=None, user_signature=True):
        """ Format a standard footer for notification emails (such as pushed
            messages notification or invite emails).
            Format:
                <p>--<br />
                    Administrator
                </p>
                <div>
                    <small>Sent from <a ...>Your Company</a>
                           using <a ...>OpenERP</a>.</small>
                </div>
        """
        footer = ""
        if not user_id:
            return footer

        # Only add user signature
        user = self.pool.get("res.users").browse(cr, SUPERUSER_ID, [user_id],
                                                 context=context)[0]
        if user_signature:
            if user.signature:
                signature = user.signature
            else:
                signature = "--<br />%s" % user.name
            footer = tools.append_content_to_html(footer, signature,
                                                  plaintext=False)

        return footer
