# -*- coding: utf-8 -*-
# Copyright 2017-2019 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestWebsiteHide(TransactionCase):
    def test_website_hide(self):
        if not self.env['res.lang'].search([('code', '=', 'nl_NL')]):
            self.env['res.lang'].load_lang('nl_NL')
        self.assertIn(
            self.env['res.lang'].search([('code', '=', 'nl_NL')]),
            self.env.ref('website.default_website').language_ids,
        )
