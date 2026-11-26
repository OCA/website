# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.tests.common import HttpCase, tagged

DEMO_ARCH = """
<t t-name="website_snippet_country_phone_code_dropdown.test_page">
    <t t-call="website.layout">
        <div id="wrap">
            <form action="" class="form-horizontal">
                <div class="js_enabled">
                    <t
                        t-call="website_snippet_country_phone_code_dropdown.dropdown_element_form"
                    />
                </div>
                <div class="js_disabled">
                    <t
                        t-call="website_snippet_country_phone_code_dropdown.dropdown_element_form"
                    >
                        <t t-set="complete_field" t-value="'disabled_complete_field'"/>
                        <t
                            t-set="country_phone_code_field"
                            t-value="'disabled_country_phone_code_field'"
                        />
                        <t
                            t-set="no_country_field"
                            t-value="'disabled_no_country_field'"
                        />
                        <t t-set="readonly" t-value="True"/>
                        <t t-set="default_value_prefix" t-value="'33'"/>
                        <t t-set="default_value_number" t-value="'6 00 11 22 33'"/>
                    </t>
                </div>
                <button type="submit" class="btn btn-default">Submit</button>
            </form>
        </div>
    </t>
</t>
"""


@tagged("post_install", "-at_install")
class TestUi(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.ref("base.user_admin").country_id = cls.env.ref("base.us")
        website = cls.env["website"].get_current_website()
        url = "/website_snippet_country_phone_code_dropdown.test_page"
        view = cls.env["ir.ui.view"].create(
            {
                "name": "Country phone code dropdown snippet test",
                "type": "qweb",
                "arch": DEMO_ARCH,
                "key": "website_snippet_country_phone_code_dropdown.test_page",
            }
        )
        page = cls.env["website.page"].create(
            {
                "url": url,
                "view_id": view.id,
                "website_id": website.id,
                "is_published": True,
            }
        )
        cls.env["website.menu"].create(
            {
                "name": "Country Phone Code Dropdown Demo",
                "url": url,
                "page_id": page.id,
                "parent_id": website.menu_id.id,
                "website_id": website.id,
                "sequence": 50,
            }
        )

    def test_01_demo_country_phone_code_dropdown_tour(self):
        self.start_tour(
            "/",
            "website_snippet_country_phone_code_dropdown_tour_demo_page",
            login="admin",
        )
