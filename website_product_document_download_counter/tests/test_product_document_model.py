# Copyright 2025 Cetmix OÜ
# License LGPL-3.0 or later (https://www.gnu.org/licenses/LGPL).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, tagged

from .product_document_test_utils import ProductDocumentTestUtils


@tagged("post_install", "-at_install")
class TestProductDocumentDownloadCounter(TransactionCase, ProductDocumentTestUtils):
    def setUp(self):
        """
        Set up the test environment by creating a product with an attached document.
        """
        super().setUp()
        self.product, self.attachment, self.document = (
            self._create_product_with_document()
        )
        self.document.write(
            {
                "active": True,
                "shown_on_product_page": True,
            }
        )

    def test_can_increment_download_count(self):
        """
        Test that the download count can be incremented when the document is active,
        """
        self.document.download_count_enabled = True
        self.document.increment_download_count()
        self.assertEqual(self.document.download_count, 1)

    def test_increment_download_count_flag_disabled(self):
        """
        Test that the download count is not incremented when the
        count_downloads flag is disabled.
        """
        self.document.download_count_enabled = False
        self.document.increment_download_count()
        self.assertEqual(self.document.download_count, 0)

    def test_increment_download_count_inactive(self):
        """
        Test that an error is raised when trying to increment
        the download count of an inactive document.
        """
        self.document.active = False
        with self.assertRaises(UserError):
            self.document.increment_download_count()
        self.assertEqual(self.document.download_count, 0)

    def test_increment_download_count_not_published(self):
        """
        Test that an error is raised when trying to increment
        the download count of a document that isn't on the product page.
        """
        self.document.shown_on_product_page = False
        self.document.download_count_enabled = True
        with self.assertRaises(UserError):
            self.document.increment_download_count()
        self.assertEqual(self.document.download_count, 0)
