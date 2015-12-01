# -*- coding: utf-8 -*-
# License AGPL-3: Antiun Ingenieria S.L. - Antonio Espinosa
# See README.rst file on addon root folder for more details

from openerp import models, fields


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    logo = fields.Binary(
        string="Website logo", related="website_id.logo",
        help="This field holds the logo for this website, showed in header."
             "Recommended size is 180x50")
