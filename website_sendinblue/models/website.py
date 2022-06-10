# Copyright 2022 Studio73 - Ioan Galan <ioan@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    sendinblue_identifier = fields.Char(
        string="Sendinblue ID",
        help="This field holds the ID, needed for Sendinblue functionality.",
    )
