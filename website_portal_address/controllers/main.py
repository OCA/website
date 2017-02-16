# -*- coding: utf-8 -*-
# Copyright 2016-Today Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp.http import request, route
from openerp.addons.website_portal_contact.controllers.main \
    import WebsiteAccount as PortalController


class WebsiteAccount(PortalController):

    @route("/my/contacts/<model('res.partner'):contact>", auth="user",
           website=True)
    def portal_my_contacts_read(self, contact):
        values = self._prepare_portal_layout_values()
        values.update({
            "state_id": request.env['res.country.state'].sudo().search([]),
            "country_id": request.env['res.country'].sudo().search([]),
            "contact": contact,
            "fields": self._contacts_fields(),
        })
        return request.website.render(
            "website_portal_contact.contacts_followup", values)

    def _contacts_fields(self):
        res = super(WebsiteAccount, self)._contacts_fields()
        res += ['type', 'street', 'street2',
                'city', 'zip',
                'country_id', 'state_id']
        return res
