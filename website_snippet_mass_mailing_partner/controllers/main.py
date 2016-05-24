# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.mass_mailing.controllers.main import MassMailController
from openerp.http import request, route


class MassMailingPartner(MassMailController):
    @route()
    def subscribe(self, list_id, email, **post):
        """Handle name if provided."""
        result = super(MassMailingPartner, self).subscribe(
            list_id, email, **post)
        name = post.get("name")
        if name:
            Contact = request.env["mail.mass_mailing.contact"].sudo()
            Partner = request.env["res.partner"].sudo()
            contacts = Contact.search([
                ("email", "=ilike", email),
                ("list_id", "=", int(list_id)),
                ("opt_out", "=", False),
            ])
            partner = Partner.search(
                [("email", "=ilike", email), ("name", "=ilike", name)],
                limit=1)
            if not partner:
                partner = Partner.create({
                    "name": name,
                    "email": email,
                })
            partner.opt_out = True
            contacts.write({
                "partner_id": partner.id,
            })
        return result
