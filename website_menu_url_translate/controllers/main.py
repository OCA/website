# -*- coding: utf-8 -*-
# Copyright 2017 initOS GmbH. <http://www.initos.com>
# Copyright 2017 GYB IT SOLUTIONS <http://www.gybitsolutions.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import werkzeug.utils
import openerp
from openerp.addons.web import http
from openerp.http import request


class Website(openerp.addons.web.controllers.main.Home):

    @http.route('/website/lang/<lang>', type='http',
                auth="public", website=True, multilang=False)
    def change_lang(self, lang, r='/', **kwargs):
        if lang == 'default':
            lang = request.website.default_lang_code
            r = '/%s%s' % (lang, r or '/')
        page_url = ''
        if lang == request.website.default_lang_code:
            page_url = str(r)
        else:
            r_value = str('/'+str(lang))
            page_url = r.replace(r_value, '')

        trans = request.env()['ir.translation'].sudo()
        search_res = trans.search([('lang', '=', str(lang)),
                                   ('src', '=', str(page_url))])

        if search_res:
            if search_res[0].value:
                r = search_res[0].value
            else:
                r = search_res[0].src

        if not r:
            ans = trans.search([('value', '=', str(page_url))])
            if ans and ans[0].id:
                src = ans[0].src
                ans2 = trans.search([('src', '=', str(src)),
                                     ('lang', '=', str(lang))])

                if ans2 and ans2[0].id:
                    if ans2.value:
                        r = ans2[0].value
                    else:
                        r = ans2[0].src
                else:
                    r = ans[0].src
        redirect = werkzeug.utils.redirect(r or ('/%s' % lang), 303)
        redirect.set_cookie('website_lang', lang)
        return redirect

    @http.route('/page/<page:page>', type='http', auth="public", website=True)
    def page(self, page, **opt):
        values = {
            'path': page,
        }

        # /page/website.XXX --> /page/XXX
        if page.startswith('website.'):
            return request.redirect('/page/' + page[8:], code=301)
        elif '.' not in page:
            page = 'website.%s' % page

        try:
            translation_obj = request.env['ir.translation']
            paths = '/page/' + page.split('.')[1]
            translation_objs = translation_obj.search([('value', '=', paths)])
            if translation_objs:
                res = (translation_objs[0].src).split('/')[-1]
                page = 'website.%s' % str(res)

            request.website.get_template(page)
        except ValueError, e:
            # page not found
            if request.website.is_publisher():
                page = 'website.page_404'
            else:
                return request.registry['ir.http']._handle_exception(e, 404)

        return request.render(page, values)


class language_dependent(http.Controller):

    @http.route(['/defaulturl'], type='json', auth="public", website=True)
    def call(self, menu_id, **post):
        cr, uid, context, registry = \
            request.cr, openerp.SUPERUSER_ID,\
            request.context, request.registry

        if menu_id:
            domain = [('res_id', '=', int(menu_id)),
                      ('lang', '=', str(context.get('lang')))]
            translate_obj = registry['ir.translation']
            translate_ids = translate_obj.search(cr, uid,
                                                 domain,
                                                 context=context)
            translate_obj.unlink(cr, uid, translate_ids, context=context)
            webmenu_obj = registry['website.menu']
            default_url = webmenu_obj.browse(cr, uid,
                                             int(menu_id),
                                             context=context).url
            return default_url

        return False
