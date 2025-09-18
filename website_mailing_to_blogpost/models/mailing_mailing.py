# Copyright 2025 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class MailingMailing(models.Model):
    _inherit = "mailing.mailing"

    blog_post_id = fields.Many2one("blog.post")
