# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SnippetPreset(models.Model):
    _name = 'snippet.preset'
    _description = 'Snipet Preset'

    snippet = fields.Char()
    name = fields.Char()
    arch = fields.Text()
