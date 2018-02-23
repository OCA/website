# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, fields, models


class SaleConfigSettings(models.TransientModel):
    _inherit = "sale.config.settings"

    alias_claim = fields.Char(
        "Claims Email Alias",
        help="Emails to this address will create a claim.",
    )

    @api.model
    def _find_default_claim_alias_id(self):
        """Find current claims alias record."""
        MailAlias = self.env["mail.alias"]
        crm_claim = self.env.ref("crm_claim.model_crm_claim")
        return (
            self.env.ref("website_portal_crm_claim.mail_alias_claim", False) or
            MailAlias.search(
                [
                    ("alias_model_id", "=", crm_claim.id),
                    ("alias_contact", "=", "everyone"),
                ],
                limit=1)[:1] or
            MailAlias.create({
                "alias_model_id": crm_claim.id,
                "alias_name": "claims",
                "alias_contact": "everyone",
            })
        )

    @api.model
    def get_default_alias_claim(self, fields):
        """Default value for claims alias."""
        return {
            "alias_claim": self._find_default_claim_alias_id().alias_name
        }

    @api.multi
    def set_alias_claim(self):
        """Save a new claims alias."""
        self._find_default_claim_alias_id().alias_name = self.alias_claim
