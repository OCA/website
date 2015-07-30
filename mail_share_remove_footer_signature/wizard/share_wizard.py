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

from openerp import models
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

UID_ROOT = 1


class MailMail(models.TransientModel):
    _inherit = 'share.wizard'

    def send_invite_email(self, cr, uid, wizard_data, context=None):
        # TDE Note: not updated because will disappear
        message_obj = self.pool.get('mail.message')
        notification_obj = self.pool.get('mail.notification')
        user = self.pool.get('res.users').browse(cr, UID_ROOT, uid)
        if not user.email:
            raise osv.except_osv(_('Email Required'), _('The current user must have an email address configured in User Preferences to be able to send outgoing emails.'))

        # TODO: also send an HTML version of this mail
        for result_line in wizard_data.result_line_ids:
            email_to = result_line.user_id.email
            if not email_to:
                continue
            subject = _('Invitation to collaborate about %s') % (wizard_data.record_name)
            body = _("Hello,\n\n")
            body += _("I have shared %s (%s) with you!\n\n") % (wizard_data.record_name, wizard_data.name)
            if wizard_data.message:
                body += "%s\n\n" % (wizard_data.message)
            if result_line.newly_created:
                body += _("The documents are not attached, you can view them online directly on my Odoo server at:\n    %s\n\n") % (result_line.share_url)
                body += _("These are your credentials to access this protected area:\n")
                body += "%s: %s" % (_("Username"), result_line.user_id.login) + "\n"
                body += "%s: %s" % (_("Password"), result_line.password) + "\n"
                body += "%s: %s" % (_("Database"), cr.dbname) + "\n"
            body += _("The documents have been automatically added to your subscriptions.\n\n")
            body += '%s\n\n' % ((user.signature or ''))
            msg_id = message_obj.schedule_with_attach(cr, uid, user.email, [email_to], subject, body, model='', context=context)
            notification_obj.create(cr, uid, {'user_id': result_line.user_id.id, 'message_id': msg_id}, context=context)

    def send_emails(self, cr, uid, wizard_data, context=None):
        _logger.info('Sending share notifications by email...')
        mail_mail = self.pool.get('mail.mail')
        user = self.pool.get('res.users').browse(cr, UID_ROOT, uid)
        if not user.email:
            raise osv.except_osv(_('Email Required'), _('The current user must have an email address configured in User Preferences to be able to send outgoing emails.'))

        # TODO: also send an HTML version of this mail
        mail_ids = []
        for result_line in wizard_data.result_line_ids:
            email_to = result_line.user_id.email
            if not email_to:
                continue
            subject = wizard_data.name
            body = _("Hello,\n\n")
            body += _("I've shared %s with you!\n\n") % wizard_data.name
            body += _("The documents are not attached, you can view them online directly on my Odoo server at:\n    %s\n\n") % (result_line.share_url)
            if wizard_data.message:
                body += '%s\n\n' % (wizard_data.message)
            if result_line.newly_created:
                body += _("These are your credentials to access this protected area:\n")
                body += "%s: %s\n" % (_("Username"), result_line.user_id.login)
                body += "%s: %s\n" % (_("Password"), result_line.password)
                body += "%s: %s\n" % (_("Database"), cr.dbname)
            else:
                body += _("The documents have been automatically added to your current Odoo documents.\n")
                body += _("You may use your current login (%s) and password to view them.\n") % result_line.user_id.login
            body += "\n\n%s\n\n" % ( (user.signature or '') )
            mail_ids.append(mail_mail.create(cr, uid, {
                    'email_from': user.email,
                    'email_to': email_to,
                    'subject': subject,
                    'body_html': '<pre>%s</pre>' % body}, context=context))
        # force direct delivery, as users expect instant notification
        mail_mail.send(cr, uid, mail_ids, context=context)
        _logger.info('%d share notification(s) sent.', len(mail_ids))
