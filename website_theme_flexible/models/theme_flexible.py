# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ThemeFlexible(models.Model):
    _name = 'theme.flexible'

    color_alpha = fields.Char(
        default='#1CC1A9'
    )
    color_beta = fields.Char(
        default='#875A7B'
    )
    color_gamma = fields.Char(
        default='#BA3C3D'
    )
    color_delta = fields.Char(
        default='#0D6759'
    )
    color_epsilon = fields.Char(
        default='#0B2E59'
    )

    @classmethod
    def _add_shades(cls, color):
        setattr(cls, 'amount_%s_lighter' % color, fields.Integer(
            default=10
        ))

        setattr(cls, 'amount_%s_light' % color, fields.Integer(
            default=5
        ))

        setattr(cls, 'amount_%s_dark' % color, fields.Integer(
            default=5
        ))

        setattr(cls, 'amount_%s_darker' % color, fields.Integer(
            default=10
        ))

    @classmethod
    def _add_font(cls, name):
        setattr(cls, 'font_%s' % name, fields.Char(
            default='Arial'
        ))
        setattr(cls, 'font_%s_google' % name, fields.Boolean())
        setattr(cls, 'font_%s_weight' % name, fields.Integer(
            default=400
        ))
        setattr(cls, 'font_%s_italic' % name, fields.Boolean())
        setattr(cls, 'font_%s_underline' % name, fields.Boolean())

    google_query = fields.Char(compute='_compute_google_query')

    @api.multi
    @api.depends(
        'font_normal', 'font_normal_weight', 'font_normal_italic',
        'font_normal_google',
        'font_code', 'font_code_weight', 'font_code_italic',
        'font_code_google',
        'font_header_1', 'font_header_1_weight', 'font_header_1_italic',
        'font_header_1_google',
        'font_header_2', 'font_header_2_weight', 'font_header_2_italic',
        'font_header_2_google',
        'font_header_3', 'font_header_3_weight', 'font_header_3_italic',
        'font_header_3_google',
        'font_header_4', 'font_header_4_weight', 'font_header_4_italic',
        'font_header_4_google',
        'font_header_5', 'font_header_5_weight', 'font_header_5_italic',
        'font_header_5_google',
        'font_header_6', 'font_header_6_weight', 'font_header_6_italic',
        'font_header_6_google'
    )
    def _compute_google_query(self):
        styles = ['normal', 'code', 'header_1', 'header_2',
                  'header_3', 'header_4', 'header_5', 'header_6']
        for theme in self:
            fonts = {}
            for style in styles:
                if theme['font_%s_google' % style]:
                    if theme['font_%s' % style] not in fonts:
                        fonts[theme['font_%s' % style]] = []
                    g_str = ''
                    g_str += str(theme['font_%s_weight' % style])
                    if theme['font_%s_italic' % style]:
                        g_str += 'i'
                    if g_str not in fonts[theme['font_%s' % style]]:
                        fonts[theme['font_%s' % style]].append(g_str)
            google_query = ''
            for font in fonts:
                google_query += font.replace(' ', '+') + ':'
                for variant in fonts[font]:
                    google_query += variant + ','
                google_query = google_query[:-1] + '|'
            google_query = google_query[:-1]
            theme.google_query = google_query

    bg_color = fields.Char(
        default='#FFFFFF'
    )
    footer_bg_color = fields.Char(
        default='#F8F8F8'
    )

    menu_logo = fields.Selection(
        selection=[
            ('left_text', 'Left / Name'),
            ('right_text', 'Right / Name'),
            ('left_logo', 'Left / Logo'),
            ('right_logo', 'Right / Logo')
        ],
        default='left_logo'
    )
    menu_alignment = fields.Selection(
        selection=[
            ('left', 'Left'),
            ('right', 'Right'),
            ('center', 'Center')
        ],
        default='right'
    )
    menu_sticky = fields.Boolean()
    menu_bg = fields.Char(
        default='#f8f8f8'
    )
    menu_color = fields.Char(
        default='#333333'
    )

    layout = fields.Selection(
        selection=[
            ('full_width', 'Full Width'),
            ('boxed', 'Boxed'),
            ('postcard', 'Postcard')
        ],
        default='full_width'
    )

    snippet_border_radius = fields.Integer(
        default=0
    )

    anchor_color = fields.Char(
        default='#337ab7'
    )
    anchor_footer_color = fields.Char(
        default='#337ab7'
    )


ThemeFlexible._add_shades('alpha')
ThemeFlexible._add_shades('beta')
ThemeFlexible._add_shades('gamma')
ThemeFlexible._add_shades('delta')
ThemeFlexible._add_shades('epsilon')

ThemeFlexible._add_font('normal')
ThemeFlexible._add_font('code')
ThemeFlexible._add_font('header_1')
ThemeFlexible._add_font('header_2')
ThemeFlexible._add_font('header_3')
ThemeFlexible._add_font('header_4')
ThemeFlexible._add_font('header_5')
ThemeFlexible._add_font('header_6')
