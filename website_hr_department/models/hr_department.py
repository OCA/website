# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class hr_department(models.Model):
    _inherit = 'hr.department'

    website_published = fields.Boolean(
        string='Available in the website',
        copy=False, default=False)
    public_info = fields.Html(
        string='Public Info')
