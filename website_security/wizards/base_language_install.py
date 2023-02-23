from odoo import models


class LanguageInstall(models.TransientModel):
    _inherit = "base.language.install"

    def lang_install(self):
        if self.user_has_groups("website_security.group_website_security_config"):
            return super(LanguageInstall, self.sudo()).lang_install()
        return super().lang_install()
