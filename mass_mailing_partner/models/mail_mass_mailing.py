# -*- coding: utf-8 -*-
##############################################################################
# License AGPL-3 - See LICENSE file on root folder for details
##############################################################################

from openerp import models, fields, api


class MailMassMailingList(models.Model):
    _inherit = 'mail.mass_mailing.list'

    partner_mandatory = fields.Boolean(string="Mandatory Partner",
                                       default=False)
    partner_category = fields.Many2one(comodel_name='res.partner.category',
                                       string="Partner Tag")
