# -*- coding: utf-8 -*-
# Copyright 2017-2019 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ResLang(models.Model):
    _inherit = 'res.lang'

    @api.constrains('active', 'translatable')
    def _update_website_languages(self):
        """force default website's language"""
        self.env.ref('website.default_website').write({
            'language_ids': [
                (6, False, self.search([('translatable', '=', 1)]).ids),
            ],

        })
