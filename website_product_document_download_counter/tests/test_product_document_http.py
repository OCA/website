# Copyright 2025 Cetmix OÜ
# License LGPL-3.0 or later (https://www.gnu.org/licenses/LGPL).

from odoo.tests.common import HttpCase, tagged
from odoo.tools import mute_logger

from odoo.addons.base.tests.common import BaseCommon

from .product_document_test_utils import ProductDocumentTestUtils

CONTROLLER_LOGGER = (
    "odoo.addons.website_product_document_download_counter.controllers.main"
)


@tagged("post_install", "-at_install")
class TestProductDocumentDownloadCounterHttp(
    BaseCommon,
    HttpCase,
    ProductDocumentTestUtils,
):
    def setUp(self):
        """
        Set up the test environment, including creating a test admin
        user and a product document.
        """
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
                    "password": "admin",
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
                "download_count_enabled": True,
            }
        )
        self.url = (
            f"/shop/{self.product_template.id}/document/" f"{self.document.id}/count"
        )

    def test_http_download_inactive_document(self):
        """
        Test that downloading an inactive document redirects to the product page
        """
        self.document.write({"active": False})
        self.authenticate("test_admin@example.com", "admin")
        response = self.url_open(self.url, allow_redirects=False)
        document = self.env["product.document"].browse(self.document.id)
        self.assertEqual(document.download_count, 0)
        self.assertEqual(response.status_code, 301)

    @mute_logger(CONTROLLER_LOGGER)
    def test_http_download_not_published(self):
        """
        Test that downloading a document not shown on the product
        page does not increment the download count
        """
        self.document.write({"shown_on_product_page": False})
        self.authenticate(self.admin_user.login, "admin")
        before_count = self.document.download_count
        response = self.url_open(self.url, allow_redirects=True)
        after_count = (
            self.env["product.document"].browse(self.document.id).download_count
        )
        # Expect 200 when document is not published but user is authorized
        self.assertEqual(response.status_code, 200)
        self.assertEqual(after_count, before_count)

    def test_http_download_counting(self):
        """
        Test that downloading a document increments the download count
        """
        self.authenticate(self.admin_user.login, "admin")
        before_count = self.document.download_count
        response = self.url_open(self.url, allow_redirects=True)
        after_count = (
            self.env["product.document"].browse(self.document.id).download_count
        )
        # Expect 200 as valid response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(after_count, before_count + 1)
