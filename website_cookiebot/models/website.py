# Copyright 2020 Trey - Antonio González <antonio@trey.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    cookiebot_dgid = fields.Char(
        string="Cookiebot Domain Group ID",
        help="Get this code from Cookiebot to enable it on the website.",
    )
