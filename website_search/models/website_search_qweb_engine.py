# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class WebsiteSearchQwebEngine(models.AbstractModel):
    _inherit = "ir.qweb"
    _name = "website.search.qweb.engine"
