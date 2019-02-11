# Copyright 2015-2017 Tecnativa - Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2019 Tecnativa - Cristina Martin R.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import odoo.tests


class UICase(odoo.tests.HttpCase):
    def test_admin_tour_marginless_gallery(self):
        self.browser_js(
            "/",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('marginless_gallery')",
            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.marginless_gallery.ready",
            login="admin")
