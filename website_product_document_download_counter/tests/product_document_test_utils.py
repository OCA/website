class ProductDocumentTestUtils:
    def _create_product_with_document(self, product_name="Test Product"):
        product = self.env["product.template"].create(
            {
                "name": product_name,
            }
        )
        attachment = self.env["ir.attachment"].create(
            {
                "name": "Test Document",
                "type": "binary",
                "datas": b"Test data",
                "res_model": "product.template",
                "res_id": product.id,
            }
        )
        document = self.env["product.document"].search(
            [("ir_attachment_id", "=", attachment.id)], limit=1
        )
        return product, attachment, document
