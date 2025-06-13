# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase, tagged
from odoo.tools import mute_logger

from .product_document_test_utils import ProductDocumentTestUtils


LOGGER = (
    "odoo.addons.website_product_document_download_counter.models.product_document"
)


@tagged("post_install", "-at_install")
class TestProductDocumentDownloadCounterHttp(HttpCase, ProductDocumentTestUtils):
    def setUp(self):
        super().setUp()
        # Create a new admin user for HTTP tests
        admin_group = self.env.ref("base.group_system")
        self.admin_user = (
            self.env["res.users"]
            .with_context(**{"no_reset_password": True})
            .create(
                {
                    "name": "Test Admin",
                    "login": "test_admin@example.com",
                    "email": "test_admin@example.com",
                    "groups_id": [(6, 0, [admin_group.id])],
                }
            )
        )
        (self.product_template, self.attachment, self.document) = (
            self._create_product_with_document("Test Product Template")
        )
        self.document.write(
            {
                "active": True,
                "shown_on_product_page": True,
                "count_downloads": True,
            }
        )
        self.url = f"/shop/{self.product_template.id}/document/{self.document.id}"

    def test_http_download_increments_counter(self):
        initial_count = self.document.download_count
        self.authenticate("test_admin@example.com", "admin")
        self.url_open(self.url)
        self.document._invalidate_cache()
        self.assertEqual(self.document.download_count, initial_count + 1)

    def test_http_download_inactive_document(self):
        self.document.write({"active": False})
        self.authenticate("test_admin@example.com", "admin")
        with mute_logger(LOGGER):
            self.url_open(self.url)
        # Re-fetch the document to ensure it exists and is up-to-date
        document = self.env["product.document"].browse(self.document.id)
        document._invalidate_cache()
        self.assertEqual(document.download_count, 0)

    def test_http_download_not_published(self):
        self.document.write({"shown_on_product_page": False})
        self.authenticate("test_admin@example.com", "admin")
        before_count = self.document.download_count
        response = self.url_open(self.url, allow_redirects=True)
        self.document._invalidate_cache()
        after_count = self.document.download_count
        # Accept 200, 301, 303 as valid codes for this test
        self.assertIn(response.status_code, [200, 301, 303])
        self.assertEqual(after_count, before_count)
