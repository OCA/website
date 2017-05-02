# -*- coding: utf-8 -*-
# Copyright 2017 initOS GmbH. <http://www.initos.com>
# Copyright 2017 GYB IT SOLUTIONS <http://www.gybitsolutions.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class website_menu(models.Model):
    _inherit = "website.menu"

    url = fields.Char(string='Url',
                      translate=True)
