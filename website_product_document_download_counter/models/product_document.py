# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class ProductDocument(models.Model):
    _inherit = "product.document"

    download_count = fields.Integer(
        default=0,
        help="Number of times this document has been downloaded",
    )

    count_downloads = fields.Boolean(
        default=False,
        help="Enable download counting for this document when published on website",
    )

    @api.model
    def increment_download_count(self, document_id):
        """Increment the download count for a specific product document."""
        document = self.browse(document_id)
        logger.info("Incrementing download count for %s", document_id)

        if not document:
            raise UserError(_("Document not found"))

        if not document.active:
            raise UserError(_("Can't download an inactive document"))

        if document.shown_on_product_page:
            document.download_count += 1
            logger.info(
                "Download count incremented for %s to %s",
                document_id,
                document.download_count,
            )

        return True

    def toggle_count_downloads(self):
        """Toggle the count_downloads field value."""
        for record in self:
            if record.shown_on_product_page:
                record.count_downloads = not record.count_downloads
        return True
