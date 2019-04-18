# Copyright 2019 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase


class UICase(HttpCase):

    def test_ui_website(self):
        """Test frontend tour."""
        tour = "website_event_filter_organizer"
        self.browser_js(
            url_path="/event",
            code="odoo.__DEBUG__.services['web_tour.tour']"
                 ".run('%s')" % tour,
            ready="odoo.__DEBUG__.services['web_tour.tour']"
                  ".tours.%s.ready" % tour,
        )
