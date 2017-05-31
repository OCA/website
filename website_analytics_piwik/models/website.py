# -*- coding: utf-8 -*-
# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    piwik_analytics_id = fields.Integer(
        'Piwik website ID', help='The ID Piwik uses to identify the website',
        default=1)
    piwik_analytics_host = fields.Char(
        'Piwik host', help='The host/path your Piwik installation is '
        'accessible by on the internet. Do not include a protocol here!\n'
        'So http[s]://[this field]/piwik.php should resolve to your piwik.php')
