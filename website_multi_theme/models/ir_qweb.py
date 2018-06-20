# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models
from .website import ASSETS_KEY


class IrQweb(models.AbstractModel):
    _inherit = 'ir.qweb'

    def _get_asset(self, xmlid, *args, **kwargs):
        """Mock the ``web.assets_frontend`` for multi-themed websites.

        This is required for the ``/website/theme_customize`` controller, which
        may redownload this view to provide a live preview of current theme
        options.
        """
        website_id = self.env.context.get("website_id")
        if xmlid == "web.assets_frontend" and website_id:
            alt_xmlid = ASSETS_KEY % website_id
            if self.env.ref(alt_xmlid, False):
                xmlid = alt_xmlid
        return super(IrQweb, self)._get_asset(xmlid, *args, **kwargs)

    # Workaround for https://github.com/odoo/odoo/pull/24429
    def _compile_directive_snippet(self, el, options):
        return super(IrQweb, self.with_context(
            search_multi_website_snippet=options.get('website_id')
        ))._compile_directive_snippet(el, options)
