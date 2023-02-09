from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.main import Home


class Website(Home):
    @http.route(
        "/website/lang/<lang>",
        type="http",
        auth="public",
        website=True,
        multilang=False,
    )
    def change_lang(self, lang, r="/", **kwargs):
        # not in 15 # r = request.website._get_relative_url(r)
        page_url = ""
        r_value = str("/" + str(lang))
        page_url = r.replace(r_value, "")
        trans = request.env()["ir.translation"].sudo()
        trans_r = r.replace(lang + "/", "")
        lang_code = request.env["res.lang"]._lang_get_code(lang)

        search_res = trans.search(
            [("lang", "=", str(lang_code)), ("src", "=", trans_r)],
            limit=1,
            order="id asc",
        )
        if search_res:
            if search_res[0].value:
                r = str("/" + str(lang)) + search_res[0].value
            else:
                r = str("/" + str(lang)) + search_res[0].src
        if not search_res:
            trans_term_val = trans.search([("value", "=", str(page_url))])
            if not trans_term_val:
                trans_term_val = trans.search([("src", "=", str(page_url))])
            if trans_term_val and trans_term_val[0].id:
                src = trans_term_val[0].src
                trans_term_src = trans.search(
                    [("src", "=", str(src)), ("lang", "=", str(lang_code))], limit=1
                )
                if trans_term_src and trans_term_src[0].id:
                    if trans_term_src.value:
                        r = trans_term_src[0].value
                    else:
                        r = trans_term_src[0].src
                else:
                    r = trans_term_val[0].src
        return super(Website, self).change_lang(lang=lang, r=r, **kwargs)
