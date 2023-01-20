##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    has_matomo_analytics = fields.Boolean(
        "Matomo Analytics",
        related=["website_id", "has_matomo_analytics"],
        readonly=False,
    )
    matomo_analytics_id = fields.Char(
        related=["website_id", "matomo_analytics_id"], readonly=False
    )
    matomo_analytics_host = fields.Char(
        related=["website_id", "matomo_analytics_host"], readonly=False
    )
