# -*- coding: utf-8 -*-
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class WebsiteTheme(models.Model):
    _name = 'website.theme'
    _order = "name"
    _sql_constraints = [
        ("name_uniq", "UNIQUE(name)", "Name must be unique"),
    ]

    name = fields.Char(
        required=True,
        translate=True,
    )
    converted_theme_addon = fields.Char(
        help="Name of the theme addon that is being converted from single to "
             "multi website mode.",
    )
    asset_ids = fields.One2many(
        comodel_name="website.theme.asset",
        inverse_name="theme_id",
        string="Assets",
        help="Asset views that will be disabled by default and enabled only "
             "in websites that enable this theme in multiwebsite mode.",
    )

    def _convert_assets(self):
        """Generate assets for converted themes"""
        Asset = self.env["website.theme.asset"]
        for one in self.filtered("converted_theme_addon"):
            # Get all views owned by the converted theme addon
            refs = self.env["ir.model.data"].search([
                ("module", "=", one.converted_theme_addon),
                ("model", "=", "ir.ui.view"),
            ])
            existing = frozenset(one.mapped("asset_ids.name"))
            expected = frozenset(refs.mapped("complete_name"))
            dangling = tuple(existing - expected)
            # Create a new asset for each theme view
            for ref in expected - existing:
                _logger.debug("Creating asset %s for theme %s", ref, one.name)
                one.asset_ids |= Asset.new({
                    "name": ref,
                })
            # Delete all dangling assets
            if dangling:
                _logger.debug(
                    "Removing dangling assets for theme %s: %s",
                    one.name, dangling)
                Asset.search([("name", "in", dangling)]).unlink()
        # Turn all assets multiwebsite-only
        Asset._find_and_deactivate_views()


class WebsiteThemeAsset(models.Model):
    _name = "website.theme.asset"
    _sql_constraints = [
        ("name_theme_uniq", "UNIQUE(name, theme_id)",
         "Name must be unique in each theme"),
    ]

    name = fields.Char(
        name="Reference",
        required=True,
        help="External ID of the assets view that inherits from "
             "`website.assets_frontend` and adds the theme requirements.",
    )
    theme_id = fields.Many2one(
        comodel_name="website.theme",
        string="Theme",
        required=True,
        ondelete="cascade",
    )
    view_id = fields.Many2one(
        comodel_name="ir.ui.view",
        string="Assets view",
        help="View that will be enabled when this theme is used in any "
             "website, and disabled otherwise. Usually used to load assets.",
    )

    @api.model
    def _find_and_deactivate_views(self):
        """Find available views and make them multiwebsite-only."""
        linkable = self.search([
            "|", ("view_id", "=", False), ("view_id.active", "=", True),
        ])
        for one in linkable:
            try:
                one.view_id = self.env.ref(one.name)
                _logger.debug(
                    "Found view with ref %s: %r",
                    one.name,
                    one.view_id,
                )
            except ValueError:
                one.view_id = False
                _logger.debug("Ref not found: %s", one.name)
            else:
                if one.view_id.active:
                    _logger.debug("Deactivating view %s", one.name)
                    # Disable it and set it to be enabled in multi theme mode
                    one.view_id.write({
                        "active": False,
                        "was_active": True,
                    })
        # Clean Qweb cache
        IrQweb = self.env["ir.qweb"]
        IrQweb._get_asset_content.clear_cache(IrQweb)
