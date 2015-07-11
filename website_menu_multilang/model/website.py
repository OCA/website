# -*- coding: utf-8 -*-
# This file is part of OpenERP. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.


from openerp.osv import orm, fields


class WebsiteMenu(orm.Model):
    _inherit = 'website.menu'

    _columns = {
        'lang_ids': fields.many2many(
            'res.lang', 'website_menu_lang_rel', 'menu_id', 'lang_id',
            'Allowed Languages',
            help="Website languages this menu should be available for. "
            "If kept empty, it will be available for all languages"
        ),
    }

    def _default_lang_ids(self, cr, uid, context=None):
        to_ret = []

        website = self.pool.get('website').get_current_website(
            cr, uid, context)
        if website and website.default_lang_id:
            to_ret = [(4, website.default_lang_id.id)]

        return to_ret

    _defaults = {
        'lang_ids': _default_lang_ids,
    }

    def available_in_lang(self, request_lang):
        """
        Check if menu is available in specific Language

         :param string request_lang: language code to check against
        """
        # if language code is not resolved show menu by default
        if not request_lang or not self.lang_ids:
            return True

        for lang in self.lang_ids:
            if lang.code == request_lang:
                return True

        return False
