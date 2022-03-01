# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    gamification_badge_ids = fields.Many2many(
        string="Badges",
        comodel_name="gamification.badge.user",
        compute="_compute_gamification_badge_ids",
        store=True,
    )
    has_related_users = fields.Boolean(compute="_compute_has_related_users")

    @api.depends("user_ids.badge_ids", "child_ids", "child_ids.gamification_badge_ids")
    def _compute_gamification_badge_ids(self):
        for sel in self:
            sel.gamification_badge_ids = (
                sel.user_ids.mapped("badge_ids") if sel.user_ids else False
            )
            if sel.user_ids and sel != sel.commercial_partner_id:
                badges = [(4, badge) for badge in sel.user_ids.mapped("badge_ids").ids]
                sel.commercial_partner_id.gamification_badge_ids = badges

    def _compute_has_related_users(self):
        for sel in self:
            sel.has_related_users = any(a.active for a in sel.user_ids)

    def action_grant_badge_wizard(self):
        user_hr_gamification_module = self.env["ir.module.module"].search(
            [("name", "=", "user_hr_gamification")]
        )
        if (
            not user_hr_gamification_module
            or user_hr_gamification_module.state != "installed"
        ) and "employee_id" in self.env["gamification.badge.user.wizard"]._fields:
            raise ValidationError(
                _(
                    "Both hr_gamification and website_membership_gamification "
                    "modules are installed. You need to install "
                    "user_hr_gamification in order to use both."
                )
            )
        if not self.has_related_users:
            raise ValidationError(_("The partner has no related users."))
        user_id = self.user_ids.filtered(lambda a: a.active)[0]
        view_id = self.env.ref(
            "website_membership_gamification.partner_view_badge_wizard_reward"
        )
        return {
            "name": _("Reward"),
            "view_mode": "form",
            "res_model": "gamification.badge.user.wizard",
            "view_id": view_id.id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {"default_user_id": user_id.id},
        }
