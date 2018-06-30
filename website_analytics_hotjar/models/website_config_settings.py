# -*- coding: utf-8 -*-
# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    hotjar_analytics_id = fields.Char(
        related=['website_id', 'hotjar_analytics_id'])
