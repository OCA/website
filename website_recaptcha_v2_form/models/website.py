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
                        div_start = '<div class="g-recaptcha" data-sitekey='
                        div_end = 'data-callback="callback_success_recaptcha"'
                        div_end += ' data-expired-callback="callback_expired_recaptcha"'
                        updated_arch = view.arch_db.replace(
                            f'{div_start}"{site_key_old}" {div_end}/>',
                            f'{div_start} "{self.recaptcha_v2_site_key}" {div_end}/>',
                        )
                        view.sudo().write({"arch": updated_arch})

    def write(self, vals):
        res = super().write(vals)
        if "recaptcha_v2_site_key" in vals:
            self.update_recaptcha_v2_site_key()
        return res
