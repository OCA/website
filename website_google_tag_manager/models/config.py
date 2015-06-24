# -*- coding: utf-8 -*-

from openerp import models, fields, api


class website_config_settings(models.TransientModel):
    _inherit = 'website.config.settings'

    google_tag_key = fields.Char(related='website_id.google_tag_key')
