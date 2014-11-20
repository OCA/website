# -*- coding: utf-8 -*-
# This file is part of OpenERP. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.


from openerp.osv import orm, fields


class WebsiteMenu(orm.Model):
    _inherit = 'website.menu'

    _columns = {
        'lang_ids': fields.many2many(
            'res.lang', 'website_menu_lang_rel', 'menu_id', 'lang_id',
            'Languages',
        ),
    }

    def _default_lang_ids(self, cr, uid, context=None):
        website = self.pool.get('website').get_current_website(cr, uid, context)
        return website.default_lang_id and [(4, website.default_lang_id.id)] or []

    _defaults = {
        'lang_ids': _default_lang_ids,
    }

    def available_in_lang(self, request_lang):
        """
        Check if menu is available in specific Language

         :param string request_lang: language code to check against
        """
        # if language code is not resolved show menu by default
        if not request_lang:
            return True

        for lang in self.lang_ids:
            if lang.code == request_lang:
                return True

        return False
