# Copyright 2025 Cetmix OÜ
# License LGPL-3.0 or later (https://www.gnu.org/licenses/LGPL).

import logging

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request, route

logger = logging.getLogger(__name__)


class ProductDocumentDownloadCounterController(http.Controller):
    """
    Independent controller for document downloads with counter.
    Does not inherit from WebsiteSale to avoid readonly/read-write conflicts.
    """

    @route(
        '/shop/<model("product.template"):product_template>/document/<int:document_id>/count',
        type="http",
        auth="public",
        website=True,
        sitemap=False,
        readonly=False,
    )
    def product_document_with_counter(self, product_template, document_id):
        """
        Document download with download counter.

        Independent implementation that:
        1. Validates access (same as original method)
        2. Increments download counter
        3. Serves the file

        Args:
            product_template: Product template
            document_id: ID of the document to download

        Returns:
            HTTP response with file or redirect if error
        """
        # 1. Security validations (copied from original method)
        product_template.check_access("read")

        document = request.env["product.document"].browse(document_id).sudo().exists()

        # 2. Increment counter (our specific functionality)
        try:
            document.increment_download_count()
        except UserError as e:
            logger.warning(
                "Unable to increase downloads counter for document %s: %s",
                document_id,
                str(e),
            )
        except Exception:
            logger.exception(
                "Unexpected error increasing downloads counter for document %s: %s",
                document_id,
                "Internal server error",
            )

        # 3. Serve file (original method logic)
        return (
            request.env["ir.binary"]
            ._get_stream_from(
                document.ir_attachment_id,
            )
            .get_response(as_attachment=True)
        )
