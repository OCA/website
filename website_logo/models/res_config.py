# Copyright 2016 Tecnativa - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    logo = fields.Binary(related="website_id.logo")
