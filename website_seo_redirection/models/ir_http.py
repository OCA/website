# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import models
from openerp.http import request

from ..exceptions import NoOriginError, NoRedirectionError


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def _dispatch(self):
        """Handle SEO-redirected URLs."""
        # Only handle redirections for HTTP requests
        if not hasattr(request, "jsonrequest"):
            wsr = request.env["website.seo.redirection"]

            try:
                # Redirect user to SEO version of this URL if possible
                return wsr.redirect_auto()
            except NoRedirectionError:
                try:
                    # Make Odoo believe it is in the original controller
                    return self.reroute(wsr.find_origin())
                except NoOriginError:
                    pass

        return super(IrHttp, self)._dispatch()
