# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class IrModel(models.Model):
    """ Add ReCaptcha attr & validation to IrModel for use in forms """
    _inherit = 'ir.model'
    website_form_recaptcha = fields.Boolean(
        string='Require ReCaptcha',
        help='Requires successful ReCaptcha for form submission.',
    )
