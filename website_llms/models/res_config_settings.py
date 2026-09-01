# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    llms_txt_content = fields.Text(
        string="llms.txt Content",
        related="website_id.llms_txt_content",
        readonly=False,
        help="Content to be served at /llms.txt. This file provides information "
        "for Large Language Models (LLMs) about your website.",
    )
