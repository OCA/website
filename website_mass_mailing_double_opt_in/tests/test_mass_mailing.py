import odoo


@odoo.tests.common.tagged("post_install", "-at_install")
class TestMassMailing(odoo.tests.HttpCase):
    def test_mailing_list_opt_out(self):
        self.start_tour("/?enable_editor=1", "test_newsletter_popup", login="admin")
        self.start_tour("/", "test_double_optin_popup", login="admin")
        contacts = self.env["mailing.contact"].search(
            [("email", "=", "hello@world.com")]
        )
        self.assertTrue(contacts)
        self.assertIn("hello@world.com", contacts.email)
