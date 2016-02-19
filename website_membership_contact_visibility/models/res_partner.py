# -*- coding: utf-8 -*-
# © 2016 Michael Viriyananda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agp

from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    website_membership_published = fields.Boolean(
        string='Visible Contact Info On The Website',
        copy=False,
        default=True)
