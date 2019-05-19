# Copyright 2013-2017 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
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
        help="If checked, "
        "the menu will be displayed when the user is logged "
        "and give access.",
    )

    user_not_logged = fields.Boolean(
        string="User Not Logged",
        default=True,
        help="If checked, "
        "the menu will be displayed when the user is not logged "
        "and give access.",
    )

    @api.multi
    def _compute_visible(self):
        """Display the menu item whether the user is logged or not."""
        super()._compute_visible()
        for menu in self:
            if not menu.is_visible:
                continue

            if menu.env.user == menu.env.ref('base.public_user'):
                menu.is_visible = menu.user_not_logged
            else:
                menu.is_visible = menu.user_logged
