# -*- coding: utf-8 -*-
# Copyright 2013-2017 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _


class WebsiteMenu(models.Model):
    """Improve website.menu with adding booleans that drive
    if the menu is displayed when the user is logger or not.
    """
    _inherit = 'website.menu'

    user_logged = fields.Boolean(
        string="User Logged",
        default=True,
        help=_("If checked, "
               "the menu will be displayed when the user is logged "
               "and give access.")
    )

    user_not_logged = fields.Boolean(
        string="User Not Logged",
        default=True,
        help=_("If checked, "
               "the menu will be displayed when the user is not logged "
               "and give access.")
    )
