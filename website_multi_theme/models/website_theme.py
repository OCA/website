# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
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
    dependency_ids = fields.Many2many(
        "website.theme",
        "website_theme_dependency_rel",
        "theme1", "theme2",
        string="Sub-themes",
        help="If theme is splitted in different theme-modules, "
        "they should be in this list. \"Default theme\" should be here too "
        "in order to make some features (e.g. footer) "
        "work on each website independently",
    )
    asset_ids = fields.One2many(
        comodel_name="website.theme.asset",
        inverse_name="theme_id",
        string="Assets",
        help="Asset views that will be disabled by default and enabled only "
             "in websites that enable this theme in multiwebsite mode.",
    )
    has_assets = fields.Boolean(compute='_compute_has_assets', store=True)

    @api.multi
    @api.depends('dependency_ids', 'asset_ids')
    def _compute_has_assets(self):
        for r in self:
            r.has_assets = bool(r.get_assets())

    @api.multi
    def upstream_dependencies(self):
        """Returns the theme and all its dependencies"""
        themes = self
        while True:
            new_deps = themes.mapped('dependency_ids') - themes
            if new_deps:
                themes |= new_deps
            else:
                break
        return themes

    @api.multi
    def get_assets(self):
        """Assets of the theme and all its dependencies"""
        return self.upstream_dependencies().mapped('asset_ids')

    def _convert_assets(self):
        """Generate assets for converted themes"""
        Asset = self.env["website.theme.asset"]

        common_refs = self.env["ir.model.data"]

        # add views with customize_show menu, so we can activate them per
        # website independently
        common_refs |= self.env['ir.ui.view']\
                           .with_context(active_test=False)\
                           .search([
                               ('website_id', '=', False),
                               ('customize_show', '=', True),
                           ]).mapped('model_data_id')
        _logger.debug('common_refs: %s', common_refs.mapped('complete_name'))

        for one in self:
            refs = self.env["ir.model.data"]

            if one.converted_theme_addon:
                # Get all views owned by the converted theme addon
                refs |= self.env["ir.model.data"].search([
                    ("module", "=", one.converted_theme_addon),
                    ("model", "=", "ir.ui.view"),
                ])

            if refs or one.asset_ids:
                # add common_refs only for installed themes
                refs |= common_refs

            views = self.env["ir.ui.view"].with_context(active_test=False) \
                .search([
                    ("id", "in", refs.mapped("res_id")),
                    ("type", "=", "qweb"),
                ])
            existing = frozenset(
                one
                .mapped("asset_ids")
                .filtered("auto")
                .mapped("name")
            )
            expected = frozenset(views.mapped("xml_id"))

            dangling = tuple(existing - expected)
            # Create a new asset for each theme view
            for ref in expected - existing:
                _logger.debug("Creating asset %s for theme %s", ref, one.name)
                one.asset_ids |= Asset.new({
                    "name": ref,
                    "auto": True,
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
    _order = 'view_priority,view_id,id'
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
    view_priority = fields.Integer(
        related='view_id.priority',
        store=True,
        readonly=True,
    )
    auto = fields.Boolean(
        string="Auto-generated",
        help="Created automatically from theme view",
        default=False,
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
