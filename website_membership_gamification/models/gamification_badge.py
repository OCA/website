# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class GamificationBadge(models.Model):
    _inherit = "gamification.badge"

    badge_url = fields.Char(string="Badge URL")
    website_member_published = fields.Boolean(string="Published in member directory")
    new_tab_url = fields.Boolean(string="Open URL in new tab")
    website_expiration_date = fields.Date()
