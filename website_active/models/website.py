# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    active = fields.Boolean(default=True)

    @api.model
    def get_current_website(self, fallback=True):
        if request and request.session.get("force_website_id"):
            website_id = self.browse(request.session["force_website_id"]).exists()
            if website_id and not website_id.active:
                request.session.pop("force_website_id")
                request.session["force_website_id"] = (
                    self.env["website"].search([], limit=1).id
                )
        return super().get_current_website(fallback=fallback)
