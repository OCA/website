# Copyright 2025 Cetmix OÜ
# License LGPL-3.0 or later (https://www.gnu.org/licenses/LGPL).

from odoo import _, fields, models
from odoo.exceptions import UserError


class ProductDocument(models.Model):
    _inherit = "product.document"

    download_count = fields.Integer(
        default=0,
        readonly=True,
        copy=False,
        help="Number of times this document has been downloaded",
    )

    download_count_enabled = fields.Boolean(
        copy=False,
        help="Enable download counting for this document when published on website",
    )

    def increment_download_count(self):
        """
        Increment the download count for a specific product document.
        Caller must ensure appropriate permissions (e.g. via sudo()).
        """
        self.ensure_one()
        if not self.active:
            raise UserError(_("Can't download an inactive document"))
        if not self.shown_on_product_page:
            raise UserError(_("Can't download a document not " "shown on product page"))
        if self.download_count_enabled:
            self.write({"download_count": self.download_count + 1})

        return True
