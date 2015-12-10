# -*- coding: utf-8 -*-
# © 2014 OpenERP SA
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class WebsiteTheme(models.Model):
    _name = 'website.theme'

    name = fields.Char(require=True)
    css_slug = fields.Char(string='CSS slug', require=True)
