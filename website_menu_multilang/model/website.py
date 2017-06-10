# -*- coding: utf-8 -*-
# This file is part of OpenERP. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.


from odoo import fields, models


class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    def _default_lang_ids(self):
        to_ret = []
        website = self.env['website'].get_current_website()
        if website and website.default_lang_id:
            to_ret = [(4, website.default_lang_id.id)]

        return to_ret

    lang_ids = fields.Many2many(
        'res.lang', 'website_menu_lang_rel', 'menu_id', 'lang_id',
        'Allowed Languages',
        help="Website languages this menu should be available for. "
             "If kept empty, it will be available for all languages",
        default=_default_lang_ids
    )

    def available_in_lang(self, request_lang):
        """Check if menu is available in specific Language.

        :param string request_lang: language code to check against
        """
        # if language code is not resolved show menu by default
        if not request_lang or not self.lang_ids:
            return True

        for lang in self.lang_ids:
            if lang.code == request_lang:
                return True

        return False
