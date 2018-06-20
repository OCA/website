from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    logo = fields.Binary(
        string="Website logo",
        help="This field holds the logo for this website, showed in header. "
             "Recommended size is 180x50")
