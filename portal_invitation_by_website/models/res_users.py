from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _create_user_from_template(self, values):
        website_id = self.env.context.get("portal_invitation_website_id")
        if website_id:
            values["website_id"] = website_id
        return super()._create_user_from_template(values)
