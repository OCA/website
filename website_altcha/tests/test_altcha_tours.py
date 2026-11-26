# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.website_altcha.tests.common import Common


class TestWebsiteAltchaTours(Common):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["website.page"].create(
            {
                "name": "Altcha test page",
                "url": "/website_altcha_test",
                "key": "website_altcha.test_page_view",
                "type": "qweb",
                "is_published": True,
                "arch": """
                    <t t-call="website.layout">
                        <form class="website_altcha_form">
                            <div>
                                <button type="submit">Submit</button>
                            </div>
                        </form>
                    </t>
                """,
            }
        )
        cls.admin_user = cls.env["res.users"].search([("login", "=", "admin")], limit=1)
        cls.admin_user.partner_id.write({"email": "admin"})

    def test_contact_tour(self):
        """
        Run the contact test tour
        """
        self.start_tour("/contactus", "website_altcha_contact")

    def test_signup_tour(self):
        """
        Run the signup test tour
        """
        self.start_tour("/web/reset_password", "website_altcha_signup")

    def test_login_tour(self):
        """
        Run the login test tour. Redirect to the portal to avoid loading the backend,
        which can exceed the tour's 20s unload timeout on slow CI
        """
        self.start_tour("/web/login?redirect=/my", "website_altcha_login")

    def test_generic_tour(self):
        """
        Run the generic test tour
        """
        self.start_tour("/website_altcha_test", "website_altcha_generic")
