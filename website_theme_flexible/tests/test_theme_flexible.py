# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestThemeFlexible(TransactionCase):
    def setUp(self):
        super(TestThemeFlexible, self).setUp()
        self.theme = self.env.ref('website_theme_flexible.'
                                  'default_theme_flexible')

    def test_google_query(self):
        self.theme.font_normal = 'Lato'
        self.theme.font_normal_weight = 400
        self.theme.font_normal_google = True
        self.theme.font_normal_italic = True

        self.theme.font_code = 'Lato'
        self.theme.font_code_weight = 400
        self.theme.font_code_google = True
        self.theme.font_code_italic = True

        self.theme.font_header_1 = 'Mina'
        self.theme.font_header_1_weight = 700
        self.theme.font_header_1_google = True

        self.assertTrue(self.theme.google_query == 'Lato:400i|Mina:700' or
                        self.theme.google_query == 'Mina:700|Lato:400i')
