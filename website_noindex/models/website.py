from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    no_index = fields.Boolean(
        string="Disallow the site to appear in search engines like Google and Bing."
    )


class WebsiteConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    no_index = fields.Boolean(
        related="website_id.no_index",
        readonly=False,
        string="Disallow the site to appear in search engines like Google and Bing.",
    )
