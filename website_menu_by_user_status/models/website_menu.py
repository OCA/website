# Copyright 2013-2017 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WebsiteMenu(models.Model):
    """Improve website.menu with adding booleans that drive
    if the menu is displayed when the user is logger or not.
    """

    _inherit = "website.menu"

    user_logged = fields.Boolean(
        string="Visible for logged Users",
        default=True,
        help="If checked, "
        "the menu will be displayed when the user is logged "
        "and give access.",
    )

    user_not_logged = fields.Boolean(
        string="Visible for public Users",
        default=True,
        help="If checked, "
        "the menu will be displayed when the user is not logged "
        "and give access.",
    )

    def _compute_visible(self):
        # pylint: disable=missing-return
        """Display the menu item whether the user is logged or not."""
        super()._compute_visible()
        for menu in self:
            if not menu.is_visible:
                continue

            if self.env.user == self.env.ref("base.public_user"):
                menu.is_visible = menu.user_not_logged
            else:
                menu.is_visible = menu.user_logged
