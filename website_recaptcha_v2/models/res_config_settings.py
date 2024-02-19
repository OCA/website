# SPDX-FileCopyrightText: 2010-2014 Elico Corp
# SPDX-FileContributor: Augustin Cisterne-Kaas <augustin.cisterne-kaas@elico-corp.com>
# SPDX-FileCopyrightText: 2015 Tech-Receptives Solutions Pvt. Ltd.
# SPDX-FileCopyrightText: 2019 Simone Orsi - Camptocamp SA
# SPDX-FileCopyrightText: 2019 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    recaptcha_v2_enabled = fields.Boolean(
        related="website_id.recaptcha_v2_enabled", readonly=False
    )
    recaptcha_v2_site_key = fields.Char(
        related="website_id.recaptcha_v2_site_key", readonly=False
    )
    recaptcha_v2_secret_key = fields.Char(
        related="website_id.recaptcha_v2_secret_key", readonly=False
    )
