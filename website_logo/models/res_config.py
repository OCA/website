# -*- coding: utf-8 -*-
# © 2015 Agile Business Group sagl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    logo = fields.Binary(
        string="Website logo", related="website_id.logo",
        help="This field holds the logo for this website, showed in header."
             "Recommended size is 180x50")
