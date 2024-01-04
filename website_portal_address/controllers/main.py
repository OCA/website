# Copyright 2016-Today Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo.http import request
from odoo.addons.website_portal_contact.controllers.main import WebsiteAccount

_logger = logging.getLogger(__name__)


class PortalAddress (WebsiteAccount):

    def _contact_get_page_view_values(self, contact, access_token, **kwargs):
        values = super()._contact_get_page_view_values(contact, access_token, **kwargs)
        values.update(
            {
                "state_id": request.env["res.country.state"].sudo().search([]),
                "country_id": request.env["res.country"].sudo().search([]),
            }
        )
        return values

    def _contacts_fields(self):
        res = super()._contacts_fields()
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
        # Validate the new fields before cleaning values
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
        return super()._contacts_clean_values(values, contact=contact)
