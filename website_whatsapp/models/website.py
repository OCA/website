# Copyright 2022 WesurRV - Shivam Kachhia <shivamkachhia04@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    whatsapp_number = fields.Char(string="WhatsApp number")
    whatsapp_text = fields.Char(
        "Default text for Whatsapp",
        help="Default text to send as message",
    )
    whatsapp_track_url = fields.Boolean(
        "Track URL",
        help="Indicate in the user's message the URL of the page from which it "
        "was sent",
    )
