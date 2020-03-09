# Copyright 2016-Today Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo.http import request, route
from odoo.addons.website_portal_contact.controllers.main import WebsiteAccount

_logger = logging.getLogger(__name__)


class WebsiteAccount(WebsiteAccount):
    @route(
        "/my/contacts/<model('res.partner'):contact>",
        auth="user",
        website=True,
    )
    def portal_my_contacts_read(self, contact, access_token=None, **kw):
        values = self._contact_get_page_view_values(contact, access_token, **kw)
        values.update(
            {
                "state_id": request.env["res.country.state"].sudo().search([]),
                "country_id": request.env["res.country"].sudo().search([]),
            }
        )
        return request.render(
            "website_portal_contact.contacts_followup", values
        )

    def _contacts_fields(self):
        res = super(WebsiteAccount, self)._contacts_fields()
        res += [
            "type",
            "street",
            "street2",
            "city",
            "zip",
            "country_id",
            "state_id",
        ]
        return res

    def _contacts_clean_values(self, values, contact=False):
        """Set values to a write-compatible format"""
        if "state_id" not in values:
            # Force erase the data
            values["state_id"] = False
        elif values["state_id"]:
            try:
                values["state_id"] = int(values["state_id"].split('-', 1)[1])
            except ValueError:
                _logger.warning('Cannot parse "state_id" : %s' % (values["state_id"]))

        if "country_id" in values and values["country_id"]:
            try:
                values["country_id"] = int(values["country_id"])
            except ValueError:
                _logger.warning(
                    'Cannot parse "country_id" : %s' % (values["country_id"]))

        result = {k: v or False for k, v in values.items()}
        result.setdefault("type", "contact")
        if not contact or contact.id != request.env.user.commercial_partner_id.id:
            result.setdefault(
                "parent_id", request.env.user.commercial_partner_id.id
            )
        return result
