from odoo import fields, models


class WebsiteDynamicLink(models.Model):
    _name = "website.dynamic.link"
    _description = "Website Dynamic Link"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    url = fields.Char(required=True)
    website_id = fields.Many2one("website")

    icon = fields.Image("Logo", max_height=128, max_width=128, required=True)
