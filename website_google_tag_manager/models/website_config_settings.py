# -*- coding: utf-8 -*-
# Copyright 2016 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    google_tag_manager_key = fields.Char(
        related=['website_id', 'google_tag_manager_key'])
