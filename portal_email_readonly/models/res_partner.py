from odoo import _, models
from odoo.exceptions import UserError


class Partner(models.Model):
    _inherit = "res.partner"

    def can_edit_email(self):
        """Can't edit `email` if there is 'base.group_portal'."""
        return not self.env.user.has_group("base.group_portal")

    def write(self, vals):
        ctx = self.env.context
        for obj in self:
            if not ctx.get("website_id", False):
                if (
                    obj.user_ids
                    and obj.user_ids[0].has_group("base.group_portal")
                    and "email" in vals
                ):
                    raise UserError(
                        _(
                            "You cannot change the email address of a portal user. "
                            "Please create a new contact person!"
                        )
                    )
        return super(Partner, self).write(vals)
