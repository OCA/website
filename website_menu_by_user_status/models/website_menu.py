# Copyright 2013-2017 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# Copyright 2018 Numigi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WebsiteMenu(models.Model):
    """Improve website.menu with adding booleans that drive
    if the menu is displayed when the user is logger or not.
    """

    _inherit = 'website.menu'

    user_logged = fields.Boolean(
        string="User Logged",
        default=True,
        help="If checked, the menu will be displayed when the user is logged."
    )

    user_not_logged = fields.Boolean(
        string="User Not Logged",
        default=True,
        help="If checked, the menu will be displayed "
             "when the user is not logged."
    )

    @api.one
    def _compute_visible(self):
        """Display the menu item whether the user is logged or not."""
        super()._compute_visible()
        if not self.is_visible:
            return

        if self.env.user == self.env.ref('base.public_user'):
            self.is_visible = self.user_not_logged
        else:
            self.is_visible = self.user_logged


class WebsiteMenuVisibleForSpecificGroups(models.Model):
    """Optionally display the menu item for a given list of user groups."""

    _inherit = 'website.menu'

    group_ids = fields.Many2many(
        'res.groups', 'website_menu_group_rel', 'menu_id', 'group_id', 'Group',
        help="If filled, the menu item is only visible to the users "
        "from one of the selected groups."
    )

    @api.one
    def _compute_visible(self):
        """Display the menu item whether the user is logged or not."""
        super()._compute_visible()
        if not self.is_visible:
            return

        if self.group_ids:
            user_has_any_group = bool(self.env.user.groups_id & self.group_ids)
            self.is_visible = user_has_any_group
