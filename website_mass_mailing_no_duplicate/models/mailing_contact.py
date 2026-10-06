# Copyright 2026 - Today: GRAP https://www.grap.coop
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import logging

from odoo import api, models, tools
from odoo.fields import Command

_logger = logging.getLogger(__name__)


class MailingContact(models.Model):
    _inherit = "mailing.contact"

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get("mailing_contact_from_website", False):
            return super().create(vals_list)
        new_vals_list = []
        all_existing_contacts = self
        for vals in vals_list:
            existing_contacts = self.search(
                [("email_normalized", "=", tools.email_normalize(vals.get("email")))]
            )
            if existing_contacts:
                new_list_ids = vals.get("list_ids")[0][2]
                existing_list_ids = existing_contacts.mapped("list_ids").ids
                to_add_list_ids = list(set(new_list_ids) - set(existing_list_ids))
                all_existing_contacts |= existing_contacts[0]
                if to_add_list_ids:
                    _logger.info(
                        f"mailing.contact #{existing_contacts[0].id}:"
                        f" Adding new mailing list {to_add_list_ids}."
                    )
                    existing_contacts[0].write(
                        {
                            "list_ids": [
                                (Command.link(list_id)) for list_id in to_add_list_ids
                            ]
                        }
                    )
                else:
                    _logger.info(
                        f"mailing.contact #{existing_contacts[0].id}:"
                        " No mailing list to change."
                    )
            else:
                new_vals_list.append(vals)

        return super().create(new_vals_list) | all_existing_contacts
