# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    llms_txt_content = fields.Text(
        string="llms.txt Content",
        help="Content to be served at /llms.txt. This file provides information "
        "for Large Language Models (LLMs) about your website.",
        translate=False,
    )
