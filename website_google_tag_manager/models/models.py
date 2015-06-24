# -*- coding: utf-8 -*-

from openerp import models, fields, api

class google_tag_manager(models.Model):
    _inherit = 'website'

    google_tag_key = fields.Char(string="Google Tag Manager")
