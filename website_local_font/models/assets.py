# Copyright 2023 Onestein - Anjeel Haria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from odoo import models


class Assets(models.AbstractModel):
    _inherit = "web_editor.assets"

    def make_scss_customization(self, url, values):
        """
        Added handling for local fonts deletion and addition in scss
        """
        delete_attachment_id = values.pop("delete-local-font-attachment-id", None)
        if delete_attachment_id:
            delete_attachment_id = int(delete_attachment_id)
            self.env["ir.attachment"].search(
                [
                    "|",
                    ("id", "=", delete_attachment_id),
                    ("original_id", "=", delete_attachment_id),
                ]
            ).unlink()

        local_fonts = values.get("local-fonts")
        if local_fonts and local_fonts != "null":
            local_fonts = dict(re.findall(r"'([^']+)': '?(\d*)", local_fonts))
            for font_name in local_fonts:
                if local_fonts[font_name]:
                    local_fonts[font_name] = int(local_fonts[font_name])
            values["local-fonts"] = str(local_fonts).replace("{", "(").replace("}", ")")
        return super(Assets, self).make_scss_customization(url, values)
