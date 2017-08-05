# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, tools
from .website import ASSETS_KEY

from odoo.addons.base.ir.ir_qweb import IrQWeb as IrQWebOriginal


class IrQweb(models.AbstractModel):
    _inherit = 'ir.qweb'

    # We reset decorator to add website_id to cache keys.
    # args in methods cannot be moved to *args, because their names are used to compute cache key
    # TODO Remove decorator and call super when the PR is merged https://github.com/odoo/odoo/pull/18462
    @tools.conditional(
        # in non-xml-debug mode we want assets to be cached forever, and the admin can force a cache clear
        # by restarting the server after updating the source code (or using the "Clear server cache" in debug tools)
        'xml' not in tools.config['dev_mode'],
        tools.ormcache_context('xmlid', 'options.get("lang", "en_US")', 'css', 'js', 'debug', 'async', keys=["website_id"]),
    )
    def _get_asset(self, xmlid, options, css=True, js=True, debug=False, async=False, values=None):
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
        # call undecorated super method. See odoo/tools/cache.py::ormcache and http://decorator.readthedocs.io/en/stable/tests.documentation.html#getting-the-source-code
        return IrQWebOriginal._get_asset.__wrapped__(self, xmlid, options, css, js, debug, async, values)

    # everything below is workaround until the PR is merged: https://github.com/odoo/odoo/pull/18462
    def _get_template_cache_keys(self):
        res = super(IrQweb, self)._get_template_cache_keys()
        if 'website_id' not in res:
            res += ['website_id']
        return res

    # decorator is reset to add website_id to cache keys
    @tools.ormcache_context('xmlid', 'options.get("lang", "en_US")',
                            keys=["website_id"])
    def _get_asset_content(self, xmlid, options):
        # call undecorated super method
        return IrQWebOriginal._get_asset_content.__wrapped__(self, xmlid, options)
