from odoo.exceptions import AccessError, UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.tools import DotDict

from odoo.addons.website.tools import MockRequest


@tagged("post_install", "-at_install")
class TestAbTesting(TransactionCase):
    def setUp(self):
        super().setUp()
        self.homepage = self.env.ref("website.homepage")
        self.user_public = self.env.ref("base.public_user")
        self.target = self.env["ab.testing.target"].create(
            {
                "name": "More views",
                "trigger_ids": [(0, 0, {"on": "url_visit", "url": "/hello/"})],
            }
        )

    def test_create_variant(self):
        """ Test variant creation """
        variant_id = self.homepage.create_variant("Nice")
        self.assertTrue(variant_id)
        variant = self.env["ir.ui.view"].browse(variant_id)
        with self.assertRaises(UserError):
            variant.create_variant("Nice 2")
        with self.assertRaises(UserError):
            self.homepage.create_variant("Nice")

    def test_toggle_enabled(self):
        variant_id = self.homepage.create_variant("Nice")
        variant = self.env["ir.ui.view"].browse(variant_id)
        self.homepage.toggle_ab_testing_enabled()
        self.assertTrue(self.homepage.ab_testing_enabled)
        with self.assertRaises(UserError):
            variant.toggle_ab_testing_enabled()

    def test_switch_variant(self):
        variant_id = self.homepage.create_variant("Nice 1")
        variant2_id = self.homepage.create_variant("Nice 2")
        with MockRequest(self.env) as request:
            request.session = {}
            self.assertFalse(self.env["ir.ui.view"].get_active_variants().ids)
            with self.assertRaises(UserError):
                self.homepage.switch_variant(None)

            with self.assertRaises(AccessError):
                self.homepage.with_user(self.user_public).switch_variant(variant2_id)
            self.homepage.switch_variant(variant_id)
            self.assertEquals(
                request.session["ab_testing"]["active_variants"][self.homepage.id],
                variant_id,
            )
            self.assertIn(variant_id, self.env["ir.ui.view"].get_active_variants().ids)

    def test_conversion(self):
        variant_id = self.homepage.create_variant("Nice 1")
        variant = self.env["ir.ui.view"].browse(variant_id)
        self.target.trigger_ids.create_conversion(variants=variant)
        self.assertEquals(self.target.conversion_count, 1)
        self.target.open_conversion_view()
        self.target.open_conversion_graph()
        self.assertEquals(self.target.conversion_ids.target_id.id, self.target.id)

    def test_render(self):
        main = self.homepage.copy({"arch": "<p>Hello</p>"})
        variant1 = self.env["ir.ui.view"].browse(main.create_variant("Variant 1"))
        variant1.write({"arch": "<p>Variant 1</p>"})
        variant2 = self.env["ir.ui.view"].browse(main.create_variant("Variant 2"))
        variant2.write({"arch": "<p>Variant 2</p>"})
        with MockRequest(self.env) as request:
            request.session = DotDict(
                {"geoip": {"country_code": None}, "ab_testing": {"active_variants": {}}}
            )
            not_enabled = main.with_user(self.user_public).render()
            self.assertEquals(not_enabled, b"<p>Hello</p>")
            main.ab_testing_enabled = True
            enabled_1 = main.with_user(self.user_public).render()
            enabled_2 = main.with_user(self.user_public).render()
            self.assertEquals(enabled_1, enabled_2)
            variant2.unlink()
            self.assertEquals(
                b"<p>Hello</p>", main.with_user(self.user_public).render()
            )
            main.render()
            main.switch_variant(variant1.id)
            self.assertEquals(b"<p>Variant 1</p>", main.render())
