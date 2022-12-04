# SPDX-FileCopyrightText: 2010-2014 Elico Corp
# SPDX-FileContributor: Augustin Cisterne-Kaas <augustin.cisterne-kaas@elico-corp.com>
# SPDX-FileCopyrightText: 2015 Tech-Receptives Solutions Pvt. Ltd.
# SPDX-FileCopyrightText: 2019 Simone Orsi - Camptocamp SA
# SPDX-FileCopyrightText: 2019 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class WebsiteConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    recaptcha_enabled = fields.Boolean(
        related="website_id.recaptcha_enabled", readonly=False
    )
    recaptcha_key_site = fields.Char(
        related="website_id.recaptcha_key_site", readonly=False
    )
    recaptcha_key_secret = fields.Char(
        related="website_id.recaptcha_key_secret", readonly=False
    )
