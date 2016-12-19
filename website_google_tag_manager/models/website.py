# -*- coding: utf-8 -*-
# Copyright 2016 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class Website(models.Model):
    _inherit = 'website'

    google_tag_manager_key = fields.Char(u"Google Tag Manager Key")
