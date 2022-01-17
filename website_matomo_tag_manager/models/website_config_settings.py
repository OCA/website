# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    matomo_tag_manager = fields.Boolean("Matomo Tag Manager", related="website_id.matomo_tag_manager", readonly=False)
    matomo_host_name = fields.Char(string="Matomo Host", related="website_id.matomo_host_name", readonly=False)
    matomo_container_ref = fields.Char(string="Matomo Container ID", related="website_id.matomo_container_ref", readonly=False)
