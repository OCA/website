from odoo import fields, models


class Config(models.TransientModel):
    _inherit = 'res.config.settings'
    website_logo = fields.Binary(related='website_id.website_logo',
                                 readonly=False)
