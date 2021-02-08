# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    def _compute_website_url(self):
        super(ResPartner, self)._compute_website_url()
        for partner in self:
            partner.website_url = "/my/contacts/%s" % partner.id
