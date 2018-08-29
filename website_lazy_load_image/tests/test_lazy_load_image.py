# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase
from lxml import etree


class LazyLoadTest(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        arch = '<t t-name="test"><main><img src="hello.jpg"/></main></t>'
        cls.view_1 = cls.env['ir.ui.view'].create({
            'name': 'Test 1',
            'key': 'website_lazy_load_image.test_1',
            'type': 'qweb',
            'arch_base': arch,
            'mode': 'primary'
        })
        arch_2 = '<t t-name="test"><main>' \
                 '<img src="hello.jpg" class="lazyload-disable"/></main></t>'
        cls.view_2 = cls.env['ir.ui.view'].create({
            'name': 'Test 1',
            'key': 'website_lazy_load_image.test_1',
            'type': 'qweb',
            'arch_base': arch_2,
            'mode': 'primary'
        })
        cls.website_id = cls.env.ref('website.default_website').id
        cls.default_img = cls.env['ir.ui.view'].LAZYLOAD_DEFAULT_SRC

    def test_normal_render(self):
        """Check if lazy loading attributes are correctly set"""
        public_user_id = self.ref('base.public_user')
        ui_view = self.env['ir.ui.view'].sudo(
            public_user_id).with_context(website_id=self.website_id)
        res = etree.HTML(ui_view.render_template(self.view_1.id))
        imgs = res.xpath('//main//img')
        self.assertEqual(imgs[0].attrib['src'], self.default_img)
        self.assertEqual(imgs[0].attrib['data-src'], 'hello.jpg')

    def test_publisher_render(self):
        """Check if user is publisher lazy loading is disabled"""
        ui_view = self.env['ir.ui.view'].with_context(
            website_id=self.website_id)
        res = etree.HTML(ui_view.render_template(self.view_1.id))
        imgs = res.xpath('//main//img')
        self.assertTrue('data-src' not in imgs[0].attrib)
        self.assertEqual(imgs[0].attrib['src'], 'hello.jpg')

    def test_disabled_render(self):
        """Check if the class 'lazyload-disable' disables lazy
        loading
        """
        public_user_id = self.ref('base.public_user')
        ui_view = self.env['ir.ui.view'].sudo(
            public_user_id).with_context(website_id=self.website_id)
        res = etree.HTML(ui_view.render_template(self.view_2.id))
        imgs = res.xpath('//main//img')
        self.assertTrue('data-src' not in imgs[0].attrib)
        self.assertEqual(imgs[0].attrib['src'], 'hello.jpg')
