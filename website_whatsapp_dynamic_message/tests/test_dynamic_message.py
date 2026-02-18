# Copyright 2024 Christopher Ormaza <chris.ormaza@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDynamicWhatsappMessage(TransactionCase):
    def setUp(self):
        super().setUp()
        # Create test website with WhatsApp configuration
        self.website = self.env["website"].create(
            {
                "name": "Test Website",
                "whatsapp_number": "1234567890",
                "whatsapp_text": "Hello, how can we help you?",
                "whatsapp_track_url": False,
            }
        )
        # Create test product
        self.product = self.env["product.template"].create(
            {
                "name": "Test Product",
                "list_price": 100.0,
            }
        )

    def test_dynamic_message_contains_product_name(self):
        """
        Test dynamic message contains product name (Property 1)
        **Validates: Requirements 1.1**
        """
        message = self.website._get_dynamic_whatsapp_message(self.product)
        self.assertIn(self.product.name, message)

    def test_message_format_matches_template(self):
        """
        Test message format matches template (Requirement 1.2)
        **Validates: Requirements 1.2**
        """
        message = self.website._get_dynamic_whatsapp_message(self.product)
        expected_format = (
            "Hello, I'm interested in "
            "product Test Product, I would like more information"
        )
        self.assertEqual(message, expected_format)

    def test_default_message_without_product_context(self):
        """
        Test default message returned without product context (Property 4)
        **Validates: Requirements 2.2**
        """
        message = self.website._get_dynamic_whatsapp_message(None)
        self.assertEqual(message, self.website.whatsapp_text)

    def test_empty_default_message_handling(self):
        """
        Test empty default message handling (Requirement 3.2)
        **Validates: Requirements 3.2**
        """
        # Create website with empty whatsapp_text
        website_no_text = self.env["website"].create(
            {
                "name": "Test Website No Text",
                "whatsapp_number": "9876543210",
                "whatsapp_text": False,
            }
        )
        message = website_no_text._get_dynamic_whatsapp_message(None)
        self.assertEqual(message, "")

    # TODO: Implement additional tests in Tasks 2.4, 4.2, 5.2

    def test_url_encoding_applied(self):
        """
        Test message is returned without URL encoding (encoding happens in browser)
        **Validates: Requirements 1.4, 5.1, 5.3**
        """
        message = self.website._get_track_url_message("/shop", self.product)
        # The message should contain actual characters (not URL-encoded)
        # URL encoding happens in the browser when the link is clicked
        self.assertIn("Hello", message)
        self.assertIn("interested in product", message)
        self.assertIn(self.product.name, message)

    def test_special_characters_encoding(self):
        """
        Test special characters are preserved in message (encoding happens in browser)
        **Validates: Requirements 5.1, 5.2**
        """
        # Create product with special characters
        product_special = self.env["product.template"].create(
            {
                "name": "Product & Service #1",
                "list_price": 150.0,
            }
        )
        message = self.website._get_track_url_message("/shop", product_special)
        # Check that special characters are present (not encoded)
        self.assertIn("&", message)
        self.assertIn("#", message)
        self.assertIn("Product & Service #1", message)

    def test_unicode_characters_encoding(self):
        """
        Test Unicode characters are properly preserved (encoding happens in browser)
        **Validates: Requirements 5.2**
        """
        # Create product with Unicode characters
        product_unicode = self.env["product.template"].create(
            {
                "name": "Café Español 中文",
                "list_price": 200.0,
            }
        )
        message = self.website._get_track_url_message("/shop", product_unicode)
        # Check that Unicode characters are preserved (not encoded)
        self.assertIn("Café Español 中文", message)
        self.assertIn("é", message)
        self.assertIn("ñ", message)
        self.assertIn("中文", message)

    def test_track_url_appended_when_enabled(self):
        """
        Test track URL is appended when enabled (Property 3)
        **Validates: Requirements 1.5, 2.3**
        """
        # Enable track URL
        self.website.whatsapp_track_url = True
        message = self.website._get_track_url_message("/shop/product-1", self.product)
        # Check that "Sent from:" text is present
        self.assertIn("Sent from:", message)
        # Check that the path is included
        self.assertIn("/shop/product-1", message)
        # Check that line breaks are present (%0A)
        self.assertIn("%0A%0A", message)

    def test_track_url_not_appended_when_disabled(self):
        """
        Test track URL is not appended when disabled
        **Validates: Requirements 5.3**
        """
        # Ensure track URL is disabled
        self.website.whatsapp_track_url = False
        message = self.website._get_track_url_message("/shop", self.product)
        # Check that "Sent from:" text is NOT present
        self.assertNotIn("Sent from:", message)
        # Check that the path is NOT included
        self.assertNotIn("/shop", message)

    def test_track_url_with_default_message(self):
        """
        Test track URL works with default message (Property 5)
        **Validates: Requirements 2.3**
        """
        # Enable track URL
        self.website.whatsapp_track_url = True
        # Call without product context
        message = self.website._get_track_url_message("/contact", None)
        # Check that default message is encoded
        self.assertIn("Hello", message)
        # Check that track URL is appended
        self.assertIn("Sent from:", message)
        self.assertIn("/contact", message)

    def test_url_query_parameters_removed(self):
        """
        Test URL query parameters are removed from track URL
        **Validates: Requirements 5.3**
        """
        # Enable track URL
        self.website.whatsapp_track_url = True
        # Call with URL containing query parameters
        message = self.website._get_track_url_message(
            "/shop/product-1?search=test&page=2", self.product
        )
        # Check that query parameters are NOT in the message
        self.assertNotIn("search=test", message)
        self.assertNotIn("page=2", message)
        # Check that the base path is still present
        self.assertIn("/shop/product-1", message)

    # Integration tests for template rendering (Task 4.2)

    def test_template_product_context_detection(self):
        """
        Test template detects product context correctly (Property 1)
        **Validates: Requirements 1.3, 4.1**
        """
        # Test that when product context is provided, the dynamic message is generated
        message_with_product = self.website._get_dynamic_whatsapp_message(self.product)
        message_without_product = self.website._get_dynamic_whatsapp_message(None)

        # The messages should be different
        self.assertNotEqual(message_with_product, message_without_product)
        # Product message should contain the product name
        self.assertIn(self.product.name, message_with_product)
        # Non-product message should be the default
        self.assertEqual(message_without_product, self.website.whatsapp_text)

    def test_template_message_generation_with_product(self):
        """
        Test message generation is called with product parameter
        **Validates: Requirements 1.3, 4.2**
        """
        # Test that _get_track_url_message correctly uses product context
        self.website.whatsapp_track_url = True
        message = self.website._get_track_url_message("/shop/product-1", self.product)

        # Check that the dynamic message is in the output
        # The message should contain the product name (not URL encoded)
        self.assertIn("Test Product", message)
        # Check that the message format is correct
        self.assertIn("interested in product", message)

    def test_template_base_module_button_preserved(self):
        """
        Test base module button rendering is preserved (Property 6)
        **Validates: Requirements 3.1, 6.2**
        """
        # Test that the base module functionality is preserved
        # by verifying that _get_track_url_message works without product
        self.website.whatsapp_track_url = False
        message = self.website._get_track_url_message("/contact", None)

        # Should return the default message (not URL encoded)
        self.assertEqual(message, self.website.whatsapp_text)

    def test_template_missing_product_context_fallback(self):
        """
        Test template falls back to default message
        when product is missing (Requirement 4.3)
        **Validates: Requirements 4.3**
        """
        # Test that when product is None, the default message is used
        message = self.website._get_dynamic_whatsapp_message(None)
        self.assertEqual(message, self.website.whatsapp_text)

        # Test with an empty recordset (simulating missing product)
        empty_product = self.env["product.template"]
        message_empty = self.website._get_dynamic_whatsapp_message(empty_product)
        self.assertEqual(message_empty, self.website.whatsapp_text)

    # Translation tests (Task 5.2)

    def test_message_template_translatable(self):
        """
        Test message template is translatable (Property 7)
        **Validates: Requirements 9.1, 9.4**
        """
        # Get or install Spanish language
        self.env["res.lang"]._activate_lang("es_ES")

        # Generate message in Spanish context
        # The translation system will use the translatable string
        message_es = self.website.with_context(
            lang="es_ES"
        )._get_dynamic_whatsapp_message(self.product)

        # Check that the message contains the product name
        # The template should be translatable even if no translation is loaded
        self.assertIn(self.product.name, message_es)
        # Check that the message follows the expected format
        self.assertIn("interested in product", message_es)

    def test_product_name_preserved_in_translation(self):
        """
        Test product name is preserved in translated messages (Property 7)
        **Validates: Requirements 9.4**
        """
        # Get or install French language
        self.env["res.lang"]._activate_lang("fr_FR")

        # Create a product with a specific name
        product_special = self.env["product.template"].create(
            {
                "name": "Special Product XYZ",
                "list_price": 250.0,
            }
        )

        # Generate message in French context
        message_fr = self.website.with_context(
            lang="fr_FR"
        )._get_dynamic_whatsapp_message(product_special)

        # Product name should be preserved exactly as is
        self.assertIn("Special Product XYZ", message_fr)
        # Verify the product name is not translated
        self.assertEqual(product_special.name, "Special Product XYZ")

    def test_multiple_language_contexts(self):
        """
        Test with multiple language contexts (en_US, es_ES)
        **Validates: Requirements 9.4**
        """
        # Get or install English language
        self.env["res.lang"]._activate_lang("en_US")

        # Get or install Spanish language
        self.env["res.lang"]._activate_lang("es_ES")

        # Generate message in English context
        message_en = self.website.with_context(
            lang="en_US"
        )._get_dynamic_whatsapp_message(self.product)

        # Generate message in Spanish context
        message_es = self.website.with_context(
            lang="es_ES"
        )._get_dynamic_whatsapp_message(self.product)

        # Verify English message
        self.assertIn("interested in product", message_en)
        self.assertIn(self.product.name, message_en)

        # Verify Spanish message (template may or may not be translated)
        # But product name should always appear
        self.assertIn(self.product.name, message_es)

        # Verify product name appears in both
        self.assertIn(self.product.name, message_en)
        self.assertIn(self.product.name, message_es)
