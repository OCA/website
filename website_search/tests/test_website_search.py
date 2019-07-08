# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from mock import patch
from odoo.tests.common import TransactionCase
from ..controllers.main import GlobalSearch as GlobalSearchController


class TestWebsiteSearch(TransactionCase):
    def setUp(self):
        super(TestWebsiteSearch, self).setUp()

    @patch("odoo.addons.website_search.controllers.main.request")
    def test_website_sale_controllers(self, mock_request):
        mock_request.env = self.env
        controller = GlobalSearchController()
        searches = self.env["website.search"].search([])
        controller.search.original_func(controller, **{"name": "Home"})
        searches_after = self.env["website.search"].search([], order="create_date desc")
        self.assertTrue(searches < searches_after)
        self.assertIsNotNone(searches_after[0].result_ids)
