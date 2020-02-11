# -*- coding: utf-8 -*-
# Copyright 2018-2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import werkzeug

from odoo import models
from .exceptions import AccessDeniedMissingGroup
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _handle_exception(cls, exception, code=500):
        if isinstance(exception, AccessDeniedMissingGroup):
            code = 403
            request.website = exception.request.website or request.env[
                'website'].get_current_website()
            html = request.env['ir.ui.view'].render_template(
                'website.403', {
                    'request': exception.request,
                    'user': request.env.user,
                    'exception': exception, })
            return werkzeug.wrappers.Response(
                html, status=code, content_type='text/html;charset=utf-8')
        return super(IrHttp, cls)._handle_exception(
            exception=exception, code=code)

    @classmethod
    def _authenticate(cls, auth_method='user'):
        if auth_method.startswith(
                'groups_of_page(') and auth_method.endswith(')'):
            # for some reason we loose website reference.
            # website_enabled is there. website is only needed for rendering.
            request.website = request.env['website'].search([], limit=1)
            super(IrHttp, cls)._authenticate(auth_method='user')
            page = request.env.ref(auth_method[15:-1]).sudo()
            approved_for_page = bool(
                page.page_permission_ids & request.env.user.groups_id)
            if page.page_permission_ids and not approved_for_page:
                raise AccessDeniedMissingGroup(request, page)
        return super(IrHttp, cls)._authenticate(auth_method=auth_method)
