# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase
from lxml import etree
from odoo.tests import tagged
from odoo.addons.website.tools import MockRequest


@tagged('-at_install', 'post_install')
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
        arch_3 = '<t t-name="test"><span>content not wrapped</span></t>'
        cls.view_3 = cls.env['ir.ui.view'].create({
            'name': 'Test 3',
            'key': 'website_lazy_load_image.test_3',
            'type': 'qweb',
            'arch_base': arch_3,
            'mode': 'primary'
        })
        arch_4 = ('<t t-name="test"><main><span>Teléfono, means phone'
                  '</span></main></t>')
        cls.view_4 = cls.env['ir.ui.view'].create({
            'name': 'Test 4',
            'key': 'website_lazy_load_image.test_4',
            'type': 'qweb',
            'arch_base': arch_4,
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

    def test_no_wrap_content(self):
        """Check content not be wrapped into extra html tags"""
        public_user_id = self.ref('base.public_user')
        ui_view = self.env['ir.ui.view'].sudo(
            public_user_id).with_context(website_id=self.website_id)
        res = ui_view.render_template(self.view_3.id).decode('UTF-8')
        arch = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" ' \
               '"http://www.w3.org/TR/REC-html40/loose.dtd">\n' \
               '<span>content not wrapped</span>'
        self.assertEqual(res, arch)

    def test_encoding_render(self):
        """Check content is correctly enconded"""
        public_user_id = self.ref('base.public_user')
        ui_view = self.env['ir.ui.view'].sudo(
            public_user_id).with_context(website_id=self.website_id)
        res = ui_view.render_template(self.view_4.id).decode('UTF-8')
        arch = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" ' \
               '"http://www.w3.org/TR/REC-html40/loose.dtd">\n' \
               '<main><span>Teléfono, means phone</span></main>'
        self.assertEqual(res, arch)
        robots = self.env.ref('website.robots').render()
        self.assertNotIn('<html>', robots.decode('UTF-8'),
                         "Robots must not be wrapped into html DOM")

    def test_doctype_full_website_page(self):
        """ Check that at least doctype is preserved on website """
        website = self.env['website'].browse(self.website_id)
        with MockRequest(self.env, website=website, multilang=False) as req:
            req.csrf_token = lambda x: str(x)
            res = self.env.ref("website.login_layout").render({
                "request": req,
                "website": website,
                "main_object": self.env["ir.ui.view"].browse()
            })
            self.assertIn(
                '<!DOCTYPE ', res.decode('UTF-8'),
                'DOCTYPE must appear in the website view'
            )
