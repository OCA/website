# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    restrict_partner_to_company = fields.Boolean(
        help="When enabled, partner lookup and creation from website forms "
        "are restricted to the website's company."
    )
