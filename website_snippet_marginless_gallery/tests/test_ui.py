# -*- coding: utf-8 -*-
# Copyright 2015-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp.tests.common import HttpCase


class UICase(HttpCase):
    def test_admin_tour_marginless_gallery(self):
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web.Tour'].run('marginless_gallery')",
            "odoo.__DEBUG__.services['web.Tour'].tours.marginless_gallery",
            "admin")
