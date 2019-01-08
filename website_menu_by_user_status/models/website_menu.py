# Copyright 2013-2017 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class WebsiteMenu(models.Model):
    """Improve website.menu with adding booleans that drive
    if the menu is displayed when the user is logger or not.
    """

    _inherit = 'website.menu'

    user_logged = fields.Boolean(
        string="Visible for logged Users",
        default=True,
        help=_("If checked, "
               "the menu will be displayed when the user is logged "
               "and give access.")
    )

    user_not_logged = fields.Boolean(
        string="Visible for public Users",
        default=True,
        help=_("If checked, "
               "the menu will be displayed when the user is not logged "
               "and give access.")
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
