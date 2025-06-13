# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import http
from odoo.http import route

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = http.logging.getLogger(__name__)


class ProductDocumentDownloadCounterController(WebsiteSale):
    @route(
        '/shop/<model("product.template"):product_template>/document/<int:document_id>',
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def product_document(self, product_template, document_id):
        result = super().product_document(product_template, document_id)

        document = product_template.product_document_ids.browse(document_id)

        if document and document.count_downloads:
            try:
                document.with_context(no_commit=True).increment_download_count(
                    document_id
                )
            except Exception as e:
                _logger.exception(
                    "Unable to increase the downloads counter: %s", str(e)
                )

        return result
