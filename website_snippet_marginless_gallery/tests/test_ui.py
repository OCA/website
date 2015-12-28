# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import HttpCase


class UICase(HttpCase):
    def test_admin_tour_marginless_gallery(self):
        self.phantom_js(
            "/",
            "openerp.Tour.run('marginless_gallery')",
            "openerp.Tour.tours.marginless_gallery",
            "admin")
