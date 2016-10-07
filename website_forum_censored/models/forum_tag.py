# -*- coding: utf-8 -*-
# © 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models
from re import compile, IGNORECASE


class ForumTag(models.Model):
    _inherit = 'forum.tag'

    @api.model
    def create(self, values):
        phrases = self.env['forum.censored.phrase'].search([])
        for phrase in phrases:
            ptn = compile(phrase.phrase, IGNORECASE)
            if 'name' in values:
                values['name'] = ptn.sub(phrase.replacement, values['name'])
        return super(ForumTag, self).create(values)
