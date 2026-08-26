from odoo.tests.common import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestPortalPagerSizeHttp(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.users"].with_context(no_reset_password=True).create(
            {
                "name": "Portal Pager Http User",
                "login": "portal_pager_http_user",
                "email": "portal_pager_http_user@example.com",
                "password": "portal_pager_http_user",
                "groups_id": [(6, 0, [cls.env.ref("base.group_portal").id])],
            }
        )

    def test_portal_pages_accept_limit_param(self):
        """Portal routes must not crash, whatever the limit value is."""
        self.authenticate("portal_pager_http_user", "portal_pager_http_user")
        for query in ("limit=20", "limit=999999", "limit=abc"):
            response = self.url_open("/my?%s" % query)
            self.assertEqual(
                response.status_code,
                200,
                "/my?%s must render fine" % query,
            )
