# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IrModel(models.Model):
    _inherit = "ir.model"

    """(DEPRECATED) Add ReCaptcha attr & validation to IrModel for use in forms """
    website_form_recaptcha = fields.Boolean(
        string="Require ReCaptcha",
        help="(Deprecated) Requires successful ReCaptcha for form submission.",
    )
