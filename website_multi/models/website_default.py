# -*- coding: utf-8 -*-
# © 2014 OpenERP SA
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools import ormcache


class WebsiteDefault(osv.Model):
    _inherit = "website"

    @ormcache(skiparg=4)
    def _get_current_website_id(self, cr, uid, domain_name, context=None):
        ids = self.search(cr, uid, [('name', '=', domain_name)],
                          context=context)
        return ids and ids[0] or None

    def _get_menu_website(self, cr, uid, ids, context=None):
        res = []
        menus = self.pool.get('website.menu').browse(
            cr, uid, ids, context=context)
        for menu in menus:
            if menu.website_id:
                res.append(menu.website_id.id)
        # IF a menu is changed, update all websites
        return res

    def _get_menu(self, cr, uid, ids, name, arg, context=None):
        result = {}
        menu_obj = self.pool['website.menu']

        for website_id in ids:
            menu_ids = menu_obj.search(cr, uid, [
                ('parent_id', '=', False),
                ('website_id', '=', website_id),
            ], order='id', context=context)
            result[website_id] = menu_ids and menu_ids[0] or False

        return result

    _columns = {
        'menu_id': fields.function(
            _get_menu,
            relation='website.menu',
            type='many2one',
            string='Main Menu',
            store={
                'website.menu': (_get_menu_website, [
                    'sequence', 'parent_id', 'website_id'], 10)
            }
        )
    }

    def _default_user_id(self, cr, uid, x):
        return self.pool['ir.model.data'].xmlid_to_res_id(
            cr, SUPERUSER_ID, 'base.public_user')

    def _default_company_id(self, cr, uid, x):
        return self.pool['ir.model.data'].xmlid_to_res_id(
            cr, SUPERUSER_ID, 'base.main_company')

    _defaults = {
        'user_id': _default_user_id,
        'company_id': _default_company_id,
    }
