from odoo import api, fields, models


class PortalWizard(models.TransientModel):
    _inherit = "portal.wizard"

    website_id = fields.Many2one(
        comodel_name="website",
        help="Apply this website to all the contacts below. "
        "The invitation email URL will match this website's domain. "
        "Leave empty to keep each contact's current website.",
    )

    def action_apply_website(self):
        """Update website_id on all partners without modifying portal access or sending
        emails.
        """
        self.user_ids._apply_website_to_partner()
        return self._action_open_modal()


class PortalWizardUser(models.TransientModel):
    _inherit = "portal.wizard.user"

    website_id = fields.Many2one(
        comodel_name="website",
        compute="_compute_website_id",
        store=True,
        readonly=False,
    )

    @api.depends("wizard_id.website_id", "partner_id.website_id")
    def _compute_website_id(self):
        for user in self:
            user.website_id = user.wizard_id.website_id or user.partner_id.website_id

    def action_grant_access(self):
        # Apply the website before creating the user, so that the signup URL
        # sent by email is built with the website domain (see
        # `get_base_url()` override in `website`).
        self._apply_website_to_partner()
        self = self.with_context(portal_invitation_website_id=self.website_id.id)
        return super().action_grant_access()

    def action_invite_again(self):
        self._apply_website_to_partner()
        self = self.with_context(portal_invitation_website_id=self.website_id.id)
        return super().action_invite_again()

    def _apply_website_to_partner(self):
        for user in self:
            if user.website_id != user.partner_id.website_id:
                user.partner_id.website_id = user.website_id
