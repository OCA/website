# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from mock import patch
from odoo.tests.common import TransactionCase
from ..controllers.main import MainController


class TestController(TransactionCase):
    @patch('odoo.addons.website_adv_image_optimization.'
           'controllers.main.request')
    @patch('odoo.http.request')
    def test_optimize(self, request, request2):
        # Mock
        request.env = self.env
        request2.env = self.env

        attachment = self.env.ref('website.business_conference')
        size = attachment.file_size
        ctrl = MainController()
        ctrl.optimize(attachment.id, 70, 300, 300)
        attachment = self.env.ref('website.business_conference')
        new_size = attachment.file_size
        self.assertFalse(new_size == size)
