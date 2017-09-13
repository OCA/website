# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import HttpCase


class UICase(HttpCase):
    def test_ui_web(self):
        """Test backend tests."""
        self.phantom_js(
            "/web/tests?debug=assets&module=module_name",
            "",
            login="admin",
        )

    def test_ui_website(self):
        """Test frontend tour."""
        self.phantom_js(
            url_path="/?debug=assets",
            code="odoo.__DEBUG__.services['web.Tour']"
                 ".run('test_module_name', 'test')",
            ready="odoo.__DEBUG__.services['web.Tour'].tours.test_module_name",
            login="admin")
