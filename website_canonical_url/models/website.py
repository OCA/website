# Copyright 2018 Simone Orsi <simone.orsi@camptocamp.com>
# Copyright initOS GmbH 2016
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, exceptions, _
from odoo.http import request
from urllib.parse import urlparse, urljoin


class Website(models.Model):
    _inherit = 'website'

    canonical_domain = fields.Char(
        help='Canonical domain is used to build unique canonical URLs '
             'to make SEO happy.'
    )

    @api.constrains('canonical_domain')
    def _check_canonical_domain(self):
        domain = self.canonical_domain
        if domain and not urlparse(domain).scheme:
            raise exceptions.ValidationError(_(
                'Canonical domain must contain protocol `http(s)://`'
            ))

    @api.multi
    def get_canonical_url(self, req=None):
        return urljoin(
            self._get_canonical_domain(),
            self._get_canonical_relative_url(req=req)
        )

    @api.multi
    def _get_canonical_domain(self):
        self.ensure_one()
        if self.canonical_domain:
            return self.canonical_domain
        params = self.env['ir.config_parameter'].sudo()
        return params.get_param('web.base.url')

    @api.multi
    def _get_canonical_relative_url(self, req=None):
        req = req or request
        url = req.httprequest.path
        lang_path = '/'
        if req.lang != req.website.default_lang_code:
            lang_path = '/%s/' % req.lang
            # enforce language path
            url = lang_path.rstrip('/') + url
        if self._is_root_page(req.httprequest.path):
            # special case for main menu items: point always to root
            url = lang_path
        return url

    def _is_root_page(self, url):
        return (
            self.menu_id.child_id and
            self.menu_id.child_id[0].url == url
        )
