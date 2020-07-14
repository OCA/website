# Copyright 2020 ABF OSIELL <https://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    res_model_name = fields.Char(compute_sudo=True)
