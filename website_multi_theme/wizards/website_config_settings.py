# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class WebsiteConfigSettings(models.TransientModel):
    _inherit = "website.config.settings"

    multi_theme_id = fields.Many2one(related="website_id.multi_theme_id")
