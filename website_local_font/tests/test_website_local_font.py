# Copyright 2023 Onestein - Anjeel Haria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.tests import common, tagged
from odoo.tools.misc import file_path


class FontTestUtils:
    @staticmethod
    def get_test_font_file(font_file_name):
        font_file_path = file_path(f"website_local_font/examples/{font_file_name}")
        with open(font_file_path, "rb") as f:
            return base64.b64encode(f.read())


@tagged("post_install", "-at_install")  # Agregar tags para mejor control de ejecución
class TestIrAttachment(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.IrAttachment = cls.env["ir.attachment"]
        cls.Web_Editor_Assets = cls.env["web_editor.assets"]
        # Preparar datos comunes
        cls.utils = FontTestUtils()

    def setUp(self):
        super().setUp()
        # Preparar datos específicos para cada test

    def test_add_local_font_otf(self):
        """Test adding a local OTF font file."""
        font_css_attachment_id = self.IrAttachment.add_local_font(
            "Trueno-wml2", "otf", self.utils.get_test_font_file("Trueno-wml2.otf")
        )

        attachment = self.IrAttachment.browse(font_css_attachment_id)
        self.assertEqual(attachment.name, "Trueno-wml2 (local-font)")
        self.assertEqual(attachment.mimetype, "text/css")

    def test_add_local_font_ttf(self):
        """Test adding a local TTF font file."""
        font_css_attachment_id = self.IrAttachment.add_local_font(
            "RacingSansOne-Regular",
            "ttf",
            self.utils.get_test_font_file("RacingSansOne-Regular.ttf"),
        )

        attachment = self.IrAttachment.browse(font_css_attachment_id)
        self.assertEqual(attachment.name, "RacingSansOne-Regular (local-font)")
        self.assertEqual(attachment.mimetype, "text/css")

    def test_add_local_font_woff(self):
        """Test adding a local WOFF font file."""
        font_css_attachment_id = self.IrAttachment.add_local_font(
            "AmaticSC-Bold", "woff", self.utils.get_test_font_file("AmaticSC-Bold.woff")
        )

        attachment = self.IrAttachment.browse(font_css_attachment_id)
        self.assertEqual(attachment.name, "AmaticSC-Bold (local-font)")
        self.assertEqual(attachment.mimetype, "text/css")

    def test_add_local_font_and_make_scss_customization(self):
        """Test adding a local font and customizing SCSS."""
        # Setup
        font_name = "AmaticSC-Bold"
        font_css_attachment_id = self.IrAttachment.add_local_font(
            font_name, "woff", self.utils.get_test_font_file(f"{font_name}.woff")
        )

        # Test SCSS customization
        scss_file_url = "/website/static/src/scss/options/user_values.scss"
        self.Web_Editor_Assets.make_scss_customization(
            scss_file_url,
            {"local-fonts": f"('{font_name}': '{font_css_attachment_id}')"},
        )

        # Verify results
        custom_url = self.Web_Editor_Assets._make_custom_asset_url(
            scss_file_url, "web.assets_frontend"
        )
        attachment = self.IrAttachment.browse(font_css_attachment_id)
        attachment.write({"url": custom_url})

        custom_attachment = self.Web_Editor_Assets._get_custom_attachment(custom_url)
        custom_content = custom_attachment.raw.decode("utf-8")
        self.assertIn(font_name, custom_content)

    def test_delete_local_font_and_make_scss_customization(self):
        """Test deleting a local font and updating SCSS."""
        # Setup - first add a font
        font_css_attachment_id = self.IrAttachment.add_local_font(
            "AmaticSC-Bold", "woff", self.utils.get_test_font_file("AmaticSC-Bold.woff")
        )

        # Test deletion
        self.Web_Editor_Assets.make_scss_customization(
            "/website/static/src/scss/options/user_values.scss",
            {"delete-local-font-attachment-id": font_css_attachment_id},
        )

        # Verify deletion
        remaining_attachments = self.IrAttachment.search(
            [("id", "=", font_css_attachment_id)]
        )
        self.assertFalse(remaining_attachments, "Font attachment should be deleted")

    def test_make_scss_customization_with_null_fonts(self):
        """Test SCSS customization with 'null' local fonts value."""
        scss_file_url = "/website/static/src/scss/options/user_values.scss"
        self.Web_Editor_Assets.make_scss_customization(
            scss_file_url,
            {"local-fonts": "null"},
        )
        # Verificar que no hay errores cuando local-fonts es "null"
        custom_url = self.Web_Editor_Assets._make_custom_asset_url(
            scss_file_url, "web.assets_frontend"
        )
        custom_attachment = self.Web_Editor_Assets._get_custom_attachment(custom_url)
        self.assertTrue(custom_attachment.exists())

    def test_make_scss_customization_without_local_fonts(self):
        """Test SCSS customization without local fonts value."""
        scss_file_url = "/website/static/src/scss/options/user_values.scss"
        self.Web_Editor_Assets.make_scss_customization(
            scss_file_url,
            {"other-value": "test"},
        )
        # Verificar que no hay errores cuando local-fonts no está presente
        custom_url = self.Web_Editor_Assets._make_custom_asset_url(
            scss_file_url, "web.assets_frontend"
        )
        custom_attachment = self.Web_Editor_Assets._get_custom_attachment(custom_url)
        self.assertTrue(custom_attachment.exists())

    def test_make_scss_customization_multiple_fonts(self):
        """Test SCSS customization with multiple local fonts."""
        # Setup - add multiple fonts
        font1_name = "AmaticSC-Bold"
        font2_name = "Trueno-wml2"

        font1_id = self.IrAttachment.add_local_font(
            font1_name, "woff", self.utils.get_test_font_file(f"{font1_name}.woff")
        )
        font2_id = self.IrAttachment.add_local_font(
            font2_name, "otf", self.utils.get_test_font_file(f"{font2_name}.otf")
        )

        # Test SCSS customization with multiple fonts
        scss_file_url = "/website/static/src/scss/options/user_values.scss"
        local_fonts_value = (
            f"('{font1_name}': '{font1_id}', '{font2_name}': '{font2_id}')"
        )

        self.Web_Editor_Assets.make_scss_customization(
            scss_file_url,
            {"local-fonts": local_fonts_value},
        )

        # Verify results
        custom_url = self.Web_Editor_Assets._make_custom_asset_url(
            scss_file_url, "web.assets_frontend"
        )
        custom_attachment = self.Web_Editor_Assets._get_custom_attachment(custom_url)
        custom_content = custom_attachment.raw.decode("utf-8")

        # Verificar que ambas fuentes están presentes
        self.assertIn(font1_name, custom_content)
        self.assertIn(font2_name, custom_content)
        self.assertIn(str(font1_id), custom_content)
        self.assertIn(str(font2_id), custom_content)

    def test_make_scss_customization_empty_font_id(self):
        """Test SCSS customization with a font that has no ID."""
        scss_file_url = "/website/static/src/scss/options/user_values.scss"
        local_fonts_value = "('TestFont': '')"

        self.Web_Editor_Assets.make_scss_customization(
            scss_file_url,
            {"local-fonts": local_fonts_value},
        )

        # Verify results
        custom_url = self.Web_Editor_Assets._make_custom_asset_url(
            scss_file_url, "web.assets_frontend"
        )
        custom_attachment = self.Web_Editor_Assets._get_custom_attachment(custom_url)
        self.assertTrue(custom_attachment.exists())
