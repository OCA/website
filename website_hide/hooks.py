# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import SUPERUSER_ID, api


def post_init_hook(cr, _pool):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.lang']._update_website_languages()
