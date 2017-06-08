# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.mass_mailing.controllers.main import MassMailController
from openerp.http import request, route


class MassMailingPartner(MassMailController):
    @route()
    def subscribe(self, list_id, email, **post):
        """Handle name if provided."""
        Partner = request.env["res.partner"].sudo()
        name = post.get("name")

        # Update partner's name, to make it get updated in contact list later
        Partner.search([("email", "=", email)], limit=1).write({"name": name})

        return super(MassMailingPartner, self).subscribe(
            list_id, email, **post)
