from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_frontend_writable_fields(self):
        return super()._get_frontend_writable_fields() | {"firstname", "lastname"}
