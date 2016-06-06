# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import http
from openerp.http import request
from openerp.addons.website_crm.controllers.main import contactus as Contactus
from openerp.exceptions import ValidationError


class snippetContactus(Contactus):

    @http.route(['/crm/contactus'], type='http', auth="public", website=True)
    def contactus(self, **kwargs):
        try:
            res = super(snippetContactus, self).contactus(**kwargs)
        except ValidationError, e:
            kwargs.update({
                'error': e.value,
            })
            res = request.website.render(
                "website_snippet_contact_form.validation_error_page", kwargs)
        return res
