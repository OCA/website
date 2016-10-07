# -*- coding: utf-8 -*-
# © 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, exceptions
from re import compile
from sre_compile import error


class ForumCensoredPhrase(models.Model):
    _name = 'forum.censored.phrase'

    phrase = fields.Char('Phrase', required=True)
    replacement = fields.Char('Replacement', default='!@*&^#', required=True)

    @api.one
    @api.constrains('phrase')
    def _check_phrase(self):
        try:
            compile(self.phrase)
        except error:
            raise exceptions.ValidationError('Expression is not valid')
