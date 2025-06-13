# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, tagged

from .product_document_test_utils import ProductDocumentTestUtils


@tagged("post_install", "-at_install")
class TestProductDocumentDownloadCounter(TransactionCase, ProductDocumentTestUtils):
    def setUp(self):
        super().setUp()
        (self.product, self.attachment, self.document) = (
            self._create_product_with_document()
        )
        self.document.write(
            {
                "active": True,
                "shown_on_product_page": True,
            }
        )

    def test_download_count_initialization(self):
        self.assertEqual(self.document.download_count, 0)
        self.assertFalse(self.document.count_downloads)

    def test_increment_download_count(self):
        self.document.count_downloads = True
        self.document.increment_download_count(self.document.id)
        self.assertEqual(self.document.download_count, 1)

    def test_increment_download_count_inactive(self):
        self.document.active = False
        with self.assertRaises(UserError):
            self.document.increment_download_count(self.document.id)

    def test_increment_download_count_not_published(self):
        self.document.shown_on_product_page = False
        self.document.count_downloads = True
        self.document.increment_download_count(self.document.id)
        self.assertEqual(self.document.download_count, 0)

    def test_toggle_count_downloads(self):
        self.document.shown_on_product_page = True
        self.document.count_downloads = False
        self.document.toggle_count_downloads()
        self.assertTrue(self.document.count_downloads)
        self.document.toggle_count_downloads()
        self.assertFalse(self.document.count_downloads)

    def test_toggle_count_downloads_not_published(self):
        self.document.shown_on_product_page = False
        self.document.count_downloads = False
        self.document.toggle_count_downloads()
        self.assertFalse(self.document.count_downloads)
