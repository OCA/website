# Copyright 2015-2017 Tecnativa - Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2019 Tecnativa - Cristina Martin R.
# Copyright 2021 Tecnativa - Alexandre D. Díaz
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import odoo.tests


class TestUi(odoo.tests.HttpCase):
    def test_admin_tour_marginless_gallery(self):
        self.start_tour("/", "marginless_gallery", login="admin")
