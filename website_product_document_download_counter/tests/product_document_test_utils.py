# Copyright 2025 Cetmix OÜ
# License LGPL-3.0 or later (https://www.gnu.org/licenses/LGPL).

import base64


class ProductDocumentTestUtils:
    def _create_product_with_document(self, product_name="Test Product"):
        product = self.env["product.template"].create({"name": product_name})

        attachment = self.env["ir.attachment"].create(
            {
                "name": "Test Document",
                "type": "binary",
                "datas": base64.b64encode(b"Test data").decode(),
                "res_model": "product.template",
                "res_id": product.id,
            }
        )
        document = self.env["product.document"].search(
            [("ir_attachment_id", "=", attachment.id)], limit=1
        )
        assert document, "Product document was not created for the attachment"
        return product, attachment, document
