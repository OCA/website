# Copyright 2023 Onestein - Anjeel Haria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.modules.module import get_module_resource
from odoo.tests import common


def test_font_file_import(font_file_name):
    font_file_path = get_module_resource(
        "website_local_font",
        "examples",
        font_file_name,
    )
    font_file = base64.b64encode(open(font_file_path, "rb").read())
    return font_file


class TestIrAttachment(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.IrAttachment = cls.env["ir.attachment"]
        cls.Web_Editor_Assets = cls.env["web_editor.assets"]

    def test_add_local_font_otf(self):
        font_css_attachment_id = self.IrAttachment.add_local_font(
            "Trueno-wml2", "otf", test_font_file_import("Trueno-wml2.otf")
        )
        self.assertRecordValues(
            self.IrAttachment.browse(font_css_attachment_id),
            [
                {
                    "name": "Trueno-wml2 (local-font)",
                    "mimetype": "text/css",
                }
            ],
        )

    def test_add_local_font_ttf(self):
        font_css_attachment_id = self.IrAttachment.add_local_font(
            "RacingSansOne-Regular",
            "ttf",
            test_font_file_import("RacingSansOne-Regular.ttf"),
        )
        self.assertRecordValues(
            self.IrAttachment.browse(font_css_attachment_id),
            [
                {
                    "name": "RacingSansOne-Regular (local-font)",
                    "mimetype": "text/css",
                }
            ],
        )

    def test_add_local_font_woff(self):
        font_css_attachment_id = self.IrAttachment.add_local_font(
            "AmaticSC-Bold", "woff", test_font_file_import("AmaticSC-Bold.woff")
        )
        self.assertRecordValues(
            self.IrAttachment.browse(font_css_attachment_id),
            [
                {
                    "name": "AmaticSC-Bold (local-font)",
                    "mimetype": "text/css",
                }
            ],
        )

    def test_add_local_font_and_make_scss_customization(self):
        font_css_attachment_id = self.IrAttachment.add_local_font(
            "AmaticSC-Bold", "woff", test_font_file_import("AmaticSC-Bold.woff")
        )
        attachment = self.env["ir.attachment"].browse(font_css_attachment_id)
        scss_file_url = "/website/static/src/scss/options/user_values.scss"
        self.Web_Editor_Assets.make_scss_customization(
            scss_file_url,
            {"local-fonts": "('AmaticSC-Bold': '" + str(font_css_attachment_id) + ")'"},
        )
        custom_url = self.Web_Editor_Assets._make_custom_asset_url(
            scss_file_url, "web.assets_common"
        )
        attachment.write({"url": custom_url})
        custom_attachment = self.Web_Editor_Assets._get_custom_attachment(custom_url)
        custom_attachment_string = custom_attachment.raw.decode("utf-8")
        self.assertEqual(
            font_css_attachment_id, custom_attachment.id, "Local Font is added"
        )
        self.assertIn("AmaticSC-Bold", custom_attachment_string, "Local Font is added")

    def test_delete_local_font_and_make_scss_customization(self):
        font_css_attachment_id = self.IrAttachment.add_local_font(
            "AmaticSC-Bold", "woff", test_font_file_import("AmaticSC-Bold.woff")
        )
        self.Web_Editor_Assets.make_scss_customization(
            "/website/static/src/scss/options/user_values.scss",
            {"delete-local-font-attachment-id": font_css_attachment_id},
        )
        self.assertNotIn(
            font_css_attachment_id,
            self.IrAttachment.search([]).ids,
            "Local Font is deleted",
        )
