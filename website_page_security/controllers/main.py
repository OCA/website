# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from contextlib import contextmanager
from odoo import http, SUPERUSER_ID
from odoo.http import request

from odoo.addons.website.controllers.main import Website
from ..models.exceptions import AccessDeniedMissingGroup


class WebsiteExtend(Website):

    @contextmanager
    def sudo(self, uid=SUPERUSER_ID):
        old_uid = request.uid
        request.uid = uid
        old_website = request.website
        request.website = request.website.sudo(uid)
        try:
            yield
        finally:
            request.uid = old_uid
            request.website = old_website

    @http.route()
    def page(self, page, **opt):
        res = super(WebsiteExtend, self).page(page, **opt)
        if getattr(res, 'status_code', None) == 404:
            # try to access page as sudo, because we got 404 as user.
            with self.sudo():
                res_sudo = super(WebsiteExtend, self).page(page, **opt)
            # if success, that means the 404 was caused by lack of permission
            # we must also check for template not being website.page_404,
            # because that is seen as a successful response too (odoo page
            # controller returns successfully the 404 page template)
            if getattr(res_sudo, 'status_code', None) == 200 and \
                    res_sudo.template != 'website.page_404':
                # by using get_current_website it works on multiwebsite
                # instances.
                page_obj = request.env['website'].get_current_website(
                    ).sudo().get_template(page)
                # get permissions, in order to provide feedback
                raise AccessDeniedMissingGroup(request, page_obj)
        # if not 404 or if 404 and also sudo access is 404 return page.
        res.qcontext.update({'ispage': True})
        return res
