from odoo import api, models

PORTAL_WELCOME_XMLID = "auth_signup.portal_set_password_email"
WEBSITE_WELCOME_XMLID = (
    "portal_invitation_by_website.mail_template_portal_welcome_website"
)


class IrModelData(models.Model):
    _inherit = "ir.model.data"

    @api.model
    def _xmlid_to_res_model_res_id(self, xmlid, raise_if_not_found=False):
        if xmlid == PORTAL_WELCOME_XMLID and self.env.context.get(
            "portal_invitation_website_id"
        ):
            xmlid = WEBSITE_WELCOME_XMLID
        return super()._xmlid_to_res_model_res_id(xmlid, raise_if_not_found)
