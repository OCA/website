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
        for one in self.filtered("converted_theme_addon"):
            # Drop all previous assets
            one.asset_ids.unlink()
            # Get all views owned by the converted theme addon
            refs = self.env["ir.model.data"].search([
                ("module", "=", one.converted_theme_addon),
                ("model", "=", "ir.ui.view"),
            ])
            # Create a new asset for each theme view
            for ref in refs:
                one.asset_ids |= self.env["website.theme.asset"].new({
                    "name": ref.complete_name,
                })


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
        compute="_compute_view_id",
        store=True,
        help="View that will be enabled when this theme is used in any "
             "website, and disabled otherwise. Usually used to load assets.",
    )

    @api.depends("name")
    def _compute_view_id(self):
        """Get a view record from the specified reference.

        If a view is found, it will make sure it is disabled, to make it
        multiwebsite-only.
        """
        for one in self:
            try:
                one.view_id = self.env.ref(one.name)
                _logger.debug(
                    "Found asset with ref %s: %r",
                    one.name,
                    one.view_id,
                )
            except ValueError:
                one.view_id = False
                _logger.debug("Ref not found: %s", one.name)
                continue
            if one.view_id.active:
                # We need to remember this view was active
                one.view_id.was_active = True
                # Disable the main view, to make it multiwebsite-only
                one.view_id.active = False
