from odoo import models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def button_choose_theme(self):
        if self.user_has_groups("website_security.group_website_security_config"):
            return super(IrModuleModule, self.sudo()).button_choose_theme()
        return super().button_choose_theme()

    def button_refresh_theme(self):
        if self.user_has_groups("website_security.group_website_security_config"):
            return super(IrModuleModule, self.sudo()).button_refresh_theme()
        return super().button_refresh_theme()

    def button_remove_theme(self):
        if self.user_has_groups("website_security.group_website_security_config"):
            return super(IrModuleModule, self.sudo()).button_remove_theme()
        return super().button_remove_theme()
