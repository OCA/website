from odoo import fields, models


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    url = fields.Char(translate=True)


class WebsitePage(models.Model):
    _inherit = "website.page"

    url = fields.Char("Page URL", translate=True)
