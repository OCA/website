# Copyright 2023 Onestein - Anjeel Haria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


import base64

from odoo import models


class Attachment(models.Model):
    _inherit = "ir.attachment"

    def add_local_font(self, font_name, extension, file_data):
        font_attachment = self.create(
            {
                "name": f"local-font-{font_name}",
                "type": "binary",
                "datas": file_data,
                "mimetype": "font/" + extension,
                "public": True,
            }
        )
        if extension == "otf":
            font_format = "opentype"
        elif extension == "ttf":
            font_format = "truetype"
        else:
            font_format = extension
        src = "url(/web/content/%s/%s) format('%s')" % (
            font_attachment.id,
            f"local-font-{font_name}",
            font_format,
        )
        file_string = (
            "@font-face { \n" " font-family: %s; \n" "src:%s; \n" "}" % (font_name, src)
        )
        font_css_attachment = self.create(
            {
                "datas": base64.b64encode(file_string.encode("utf-8")),
                "name": f"{font_name} (local-font)",
                "type": "binary",
                "mimetype": "text/css",
                "public": True,
            }
        )
        font_attachment.original_id = font_css_attachment.id
        return font_css_attachment.id
