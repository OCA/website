# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models

try:
    import argon2
except ImportError:
    argon2 = None


class Website(models.Model):
    _inherit = "website"

    altcha_key = fields.Char()
    altcha_private_key = fields.Char()
    altcha_algorithm = fields.Selection(
        selection=lambda self: self._get_available_algorithms(),
        default="PBKDF2/SHA-512",
    )
    altcha_timeout = fields.Integer(
        default=5,
        help="Time in minutes before a captcha expires. Default is 5 minutes.",
    )
    altcha_cost = fields.Integer(
        default=5000,
        help="""Cost factor for the hashing algorithm.
        For PBKDF2, this is the number of iterations.
        Default is 5000 for PBKDF2/SHA-512.""",
    )

    def _get_available_algorithms(self):
        return [
            ("SHA256", "SHA-256 (fast, testing only)"),
            ("SHA384", "SHA-384 (fast, testing only)"),
            ("SHA512", "SHA-512 (fast, testing only)"),
            ("PBKDF2/SHA-256", "PBKDF2/SHA-256"),
            ("PBKDF2/SHA-384", "PBKDF2/SHA-384"),
            ("PBKDF2/SHA-512", "PBKDF2/SHA-512 (default, good)"),
        ]
