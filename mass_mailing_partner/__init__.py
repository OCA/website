# -*- coding: utf-8 -*-
##############################################################################
# License AGPL-3 - See LICENSE file on root folder for details
##############################################################################

from . import models
from openerp import SUPERUSER_ID


def _match_existing_contacts(cr, registry):
    contact_model = registry['mail.mass_mailing.contact']
    partner_model = registry['res.partner']
    contact_ids = contact_model.search(cr, SUPERUSER_ID, [])
    for contact in contact_model.browse(cr, SUPERUSER_ID, contact_ids):
        if contact.email:
            partner_ids = partner_model.search(
                cr, SUPERUSER_ID, [('email', '=ilike', contact.email)])
            if partner_ids:
                partner_id = partner_ids[0]
                partner_model.write(cr, SUPERUSER_ID, partner_id,
                                    {'opt_out': contact.opt_out})
                contact_model.write(cr, SUPERUSER_ID, contact.id,
                                    {'partner_id': partner_id})
