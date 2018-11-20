# -*- coding: utf-8 -*-
# Copyright 2017 Simone Orsi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    # TODO: when we'll have an advanced form for editing groups
    # we should add an handler to update flags (like `_update_menu_groups`)
    group_ids = fields.Many2many(
        comodel_name='res.groups',
    )
    user_logged = fields.Boolean(
        string="User Logged-in",
        default=True,
        help="If checked, "
             "this item will be available for logged-in users.",
        inverse='_update_menu_groups',
    )
    user_not_logged = fields.Boolean(
        string="User Not Logged-in",
        default=True,
        help="If checked, "
             "this item will be available for not logged-in users.",
        inverse='_update_menu_groups',
    )

    @property
    def menu_group_public(self):
        return self.env.ref('base.group_public')

    @property
    def menu_group_logged(self):
        return self.env.ref('base.group_portal')

    def _get_updated_groups(self):
        """Get update groups recordset for current menu item."""
        groups = self.group_ids
        if self.user_logged:
            groups |= self.menu_group_logged
        else:
            groups -= self.menu_group_logged
        if self.user_not_logged:
            groups |= self.menu_group_public
        else:
            groups -= self.menu_group_public
        return groups

    def _update_menu_groups(self):
        if self.env.context.get('ws_menu_skip_group_update'):
            return
        for item in self:
            item.group_ids = item._get_updated_groups()
