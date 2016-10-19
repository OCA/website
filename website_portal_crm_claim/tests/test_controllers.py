# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests.common import HttpCase


class UICase(HttpCase):
    def setUp(self):
        super(UICase, self).setUp()
        # See https://github.com/odoo/odoo/issues/12237#issuecomment-240528092
        with self.registry.cursor() as test_cursor:
            env = self.env(test_cursor)
            claim = env.ref("crm_claim.crm_claim_1")
            portal_user = env.ref("portal.demo_user0")
            claim.message_subscribe_users(portal_user.ids)

    def test_ui_website(self):
        """Test website portal tour."""
        tour = "odoo.__DEBUG__.services['web.Tour']"
        self.phantom_js(
            url_path="/",
            code=tour + ".run('website_portal_crm_claim', 'test')",
            ready=tour + ".tours.website_portal_crm_claim",
            login="portal")
