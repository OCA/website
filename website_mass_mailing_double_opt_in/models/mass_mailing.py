from odoo import fields, models


class MailingContactSubscription(models.Model):
    _inherit = "mailing.contact.subscription"

    access_token = fields.Char(copy=False)
    mail_language = fields.Char()
