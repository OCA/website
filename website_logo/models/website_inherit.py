from odoo import api, fields, models




class Website(models.Model):


    _inherit = 'website'

    website_logo = fields.Binary()


