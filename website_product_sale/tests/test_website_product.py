# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestController(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestController, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.uom_unit = cls.env.ref('product.product_uom_unit')

        cls.product_sale_ok = cls.env['product.template'].create({
            'name': 'Product sale ok',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'website_published': True,
            'sale_ok': True,
        })

        cls.product_no_sale = cls.env['product.template'].create({
            'name': 'Product no sale',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'website_published': True,
            'sale_ok': False,
        })

    def test_compute_website_url(self):
        """Test website_url from product.templates if sellable or not."""
        self.assertFalse('/shop/' in self.product_no_sale.website_url)
        self.assertTrue('/shop/' in self.product_sale_ok.website_url)
