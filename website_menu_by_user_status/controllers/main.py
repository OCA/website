# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.main import Home
from odoo import api

logger = logging.getLogger(__name__)


class Website(Home):

    @api.model
    def _get_pages(self):
        """
        All pages width url
        """
        return request.env['website.menu'].search([]).filtered('url')

    @api.multi
    def _check_user_access(self):
        """
        Is user logged
        """
        return request.env.user == request.website.user_id or False

    @api.multi
    def _get_suggest_page(self):
        """
        All pages accessible by the user (logged or not)
        """
        if self._check_user_access():
            return self._get_pages().filtered(lambda r: r.user_not_logged)
        else:
            return self._get_pages().filtered(lambda r: r.user_logged)

    @api.multi
    def _get_page_access(self, url):
        # active pages
        active_urls = self._get_pages()

        # compose access page url
        base_url = u'/page/'
        base_url += url

        # check users (Public or Logged)
        if self._check_user_access():
            return active_urls.filtered(
                lambda r: r.user_not_logged and r.url == base_url)
        else:
            return active_urls.filtered(
                lambda r: r.user_logged and r.url == base_url)

    @api.model
    def _check_template(self, response, page):
        template = request.env['ir.ui.view']
        try:
            template = http.request.env.ref(response.template,
                                            raise_if_not_found=False)
        except Exception:
            logger.exception("Failed to load local template %r", page)
        return template

    @api.multi
    def _default_response(self, page, **opt):
        """
        This is for custom rendering page
        :param page: requested by user
        :param opt: parameters
        :return: custom 404 or page requested
        """

        # website response
        default_response = super(Website, self).page(page, **opt)

        # accessible pages
        to_display = self._get_page_access(page)

        # bad request or access denied
        bad_request = request.render('website.404', {
            'suggest_page': self._get_suggest_page()})

        # managed pages for users are unique string
        simple_page = True
        if len(page.split('.')) > 1:
            simple_page = False

        # 404 page
        page_404 = u'page_404'

        # check template exists (avoid render 404 for page added by another
        # module like contactus_thanks page in website_crm module)
        template = self._check_template(default_response, page)

        if template and template.name == page_404 or not template:
            default_response = bad_request
        elif template and template.name == page_404 and not to_display:
            default_response = bad_request
        elif template and template.name != \
                page_404 and simple_page and not to_display:
            default_response = bad_request
        return default_response

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        # Do not return 404 for odoo backend menu
        main_menu = request.env.ref('website.main_menu',
                                    raise_if_not_found=False)
        if not main_menu:
            url = request.httprequest.referrer.split('/')[-1]
            return self._default_response(url, **kw)
        return super(Website, self).index(**kw)

    @http.route('/page/<page:page>', type='http', auth="public", website=True,
                cache=300)
    def page(self, page, **opt):
        return self._default_response(page, **opt)
