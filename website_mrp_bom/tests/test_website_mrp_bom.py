# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from mock import patch
from odoo.tests.common import SavepointCase
from ..controllers.main import WebsiteMrpBomPage


class TestController(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestController, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product_template_model = cls.env['product.template']
        cls.bom_model = cls.env['mrp.bom']
        cls.bom_line_model = cls.env['mrp.bom.line']
        cls.uom_unit = cls.env.ref('product.product_uom_unit')

        cls.product_sale_ok = cls.product_template_model.create({
            'name': 'Product sale ok',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'sale_ok': True,
        })

        cls.product_no_sale = cls.product_template_model.create({
            'name': 'Product no sale',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'sale_ok': False,
        })

        cls.bom_published_1 = cls.bom_model.create({
            'product_tmpl_id': cls.product_sale_ok.id,
            'product_id': cls.product_sale_ok.product_variant_id.id,
            'product_qty': 1,
            'type': 'normal',
            'website_published': True,
        })

        cls.bom_line_model_1 = cls.bom_line_model.create({
            'bom_id': cls.bom_published_1.id,
            'product_id': cls.product_no_sale.product_variant_id.id,
            'product_qty': 2,
        })

        cls.bom_published_2 = cls.bom_model.create({
            'product_tmpl_id': cls.product_no_sale.id,
            'product_id': cls.product_no_sale.product_variant_id.id,
            'product_qty': 1,
            'type': 'normal',
        })
        cls.bom_published_2.write({'website_published': True})

        cls.bom_line_model_2 = cls.bom_line_model.create({
            'bom_id': cls.bom_published_2.id,
            'product_id': cls.product_sale_ok.product_variant_id.id,
            'product_qty': 2,
        })

    def test_compute_website_url(self):
        """Test website_url from mrp.bom."""
        self.assertTrue('/components/' in self.bom_published_1.website_url)
        self.assertTrue('/components/' in self.bom_published_2.website_url)

    @patch('odoo.addons.website_mrp_bom.'
           'controllers.main.request')
    def test_request_mrp_bom_1(self, request):
        """Test controller for mrp_bom for a product salable with
        mrp_bom_line product not salable"""
        # Mock
        request.env = self.env

        ctrl = WebsiteMrpBomPage()
        response = ctrl.boms_detail(self.bom_published_1)
        self.assertTrue('request.render()' in str(response.name))

    @patch('odoo.addons.website_mrp_bom.'
           'controllers.main.request')
    def test_request_mrp_bom_2(self, request):
        """Test controller for mrp_bom for a product not salable with
                mrp_bom_line product salable"""
        # Mock
        request.env = self.env

        ctrl = WebsiteMrpBomPage()
        response = ctrl.boms_detail(self.bom_published_2)
        self.assertTrue('request.render()' in str(response.name))

    @patch('odoo.addons.website_mrp_bom.'
           'controllers.main.request')
    def test_request_mrp_no_bom(self, request):
        """Test controller for non existing mrp_bom """
        # Mock
        request.env = self.env

        ctrl = WebsiteMrpBomPage()
        response = ctrl.boms_detail(0)
        self.assertTrue('request.not_found()' in str(response.name))
