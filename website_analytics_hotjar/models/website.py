# -*- coding: utf-8 -*-
# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    hotjar_analytics_id = fields.Char(
        'Hotjar Site ID', help='The ID Hotjar uses to identify the website',
        default=1)
