# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from mock import patch
from odoo.tests.common import SavepointCase
from odoo import exceptions
from ..controllers.main import WebsiteProductPage


class TestController(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestController, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.uom_unit = cls.env.ref('product.product_uom_unit')

        cls.product_test = cls.env['product.template'].create({
            'name': 'Product Test',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
        })
        cls.demo_user = cls.env.ref('base.user_demo')

    def test_compute_website_url(self):
        self.assertTrue(
            '/catalog/product/' in self.product_test.website_product_url)

    @patch('odoo.addons.website_product.'
           'controllers.main.request')
    def test_request_product(self, request):
        # Mock
        request.env = self.env
        ctrl = WebsiteProductPage()
        response = ctrl.products_detail(self.product_test)
        self.assertTrue('request.render()' in str(response.name))

    @patch('odoo.addons.website_product.'
           'controllers.main.request')
    def test_request_not_found(self, request):
        # Mock
        request.env = self.env
        ctrl = WebsiteProductPage()
        response = ctrl.products_detail()
        self.assertTrue('request.not_found()' in str(response.name))

    def test_website_product_publish_button(self):
        product_page = self.product_test.website_product_publish_button()
        self.assertTrue(product_page['url'],
                        self.product_test.website_product_url)

    def test_website_product_publish_button_not_allowed(self):
        with self.assertRaises(exceptions.AccessError):
            self.product_test.sudo(
                self.demo_user).website_product_publish_button()

    @patch('odoo.addons.website_product.'
           'controllers.main.request')
    def test_request_catalog_publish(self, request):
        # Mock
        request.env = self.env
        ctrl = WebsiteProductPage()
        response = ctrl.publish(self.product_test.id, 'product.template')
        self.assertTrue(self.product_test.website_product_published, True)
        self.assertTrue(response, True)
