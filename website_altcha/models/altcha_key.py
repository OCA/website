# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AltchaKey(models.Model):
    _name = "altcha.key"
    _description = "Altcha Key"

    key = fields.Char(required=True)
    expires_at = fields.Datetime(required=True)
    used = fields.Boolean(default=False)

    _sql_constraints = [
        ("key_uniq", "unique(key)", "The Altcha key must be unique."),
    ]

    @api.autovacuum
    def _autovacuum_expired_keys(self):
        """Delete expired Altcha keys."""
        now = fields.Datetime.now()
        expired_keys = self.search([("expires_at", "<", now)])
        expired_keys.unlink()
