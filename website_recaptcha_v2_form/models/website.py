from odoo import api, models
from odoo.exceptions import AccessDenied


class Website(models.Model):
    _inherit = "website"

    def valid_recaptcha(self, values):
        valid, message = self.is_recaptcha_v2_valid(values)
        if not valid:
            raise AccessDenied(message)
        return True

    @api.model
    def get_recaptcha_v2_site_key(self):
        return self.sudo().get_current_website().recaptcha_v2_site_key

    def update_recaptcha_v2_site_key(self):
        views_recaptcha = (
            self.env["ir.ui.view"]
            .sudo()
            .search(
                [
                    ("arch_db", "ilike", 'class="g-recaptcha"'),
                    ("website_id", "!=", False),
                ]
            )
        )
        if views_recaptcha:
            for view in views_recaptcha:
                site_key_old = view.arch_db.split('data-sitekey="')
                if len(site_key_old) > 1:
                    site_key_old = site_key_old[1].split('"')[0]
                    if site_key_old:
                        updated_arch = view.arch_db.replace(
                            f'data-sitekey="{site_key_old}"',
                            f'data-sitekey="{self.recaptcha_v2_site_key}"',
                        )
                        view.sudo().write({"arch": updated_arch})

    def write(self, vals):
        res = super().write(vals)
        if "recaptcha_v2_site_key" in vals:
            self.update_recaptcha_v2_site_key()
        return res
