# Copyright 2021 Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class SlideSliode(models.Model):
    _inherit = "slide.slide"

    # Use sanitize = False to allow to use iframe in html contet
    html_content = fields.Html(
        string="HTML Content",
        help="Custom HTML content for slides of type 'Web Page'.",
        translate=True,
        sanitize_form=False,
        sanitize=False,
    )
