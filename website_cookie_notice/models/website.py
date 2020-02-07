# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    cookie_notice_legal_page_id = fields.Many2one(
        comodel_name="website.page", string="Linked legal page"
    )
