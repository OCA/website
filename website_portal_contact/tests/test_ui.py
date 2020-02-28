# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests.common import HttpCase


class UICase(HttpCase):
    def setUp(self):
        super(UICase, self).setUp()
        with self.cursor() as cr:
            env = self.env(cr)
            # Need a demo user with portal permissions
            env.ref("base.user_demo").groups_id = env.ref("base.group_portal")

    def test_contacts(self):
        """Test frontend tour."""
        self.phantom_js(
            url_path="/",
            code="odoo.__DEBUG__.services['web.Tour']"
                 ".run('website_portal_contact', 'test', 'events')",
            ready="odoo.__DEBUG__.services['web.Tour']"
                  ".tours.website_portal_contact",
            login="demo")
