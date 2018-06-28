# Copyright 2018 Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class WebsiteConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    canonical_domain = fields.Char(related='website_id.canonical_domain')
