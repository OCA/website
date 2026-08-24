from unittest.mock import patch

from odoo.tests.common import TransactionCase, users

from odoo.addons.mail.tests.common import mail_new_test_user


class TestPortalWizardWebsite(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website_1 = cls.env.ref("website.default_website")
        cls.website_2 = cls.env["website"].create(
            {
                "name": "Website 2",
                "domain": "https://www.website2.example.com",
                "specific_user_account": True,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Portal Test Partner",
                "email": "portal_test@example.com",
            }
        )
        cls.partner_with_website = cls.env["res.partner"].create(
            {
                "name": "Partner With Website",
                "email": "partner_website@example.com",
                "website_id": cls.website_1.id,
            }
        )

    def _open_wizard(self, partners):
        return (
            self.env["portal.wizard"].with_context(active_ids=partners.ids).create({})
        )

    @users("admin")
    def test_website_id_propagates_from_wizard(self):
        """website_id set at wizard level flows to all portal.wizard.user lines."""
        wizard = self._open_wizard(self.partner)
        wizard.website_id = self.website_2
        self.assertEqual(wizard.user_ids.website_id, self.website_2)

    @users("admin")
    def test_website_id_defaults_from_partner(self):
        """When wizard has no website_id, each line defaults to its partner's."""
        wizard = self._open_wizard(self.partner_with_website)
        self.assertEqual(wizard.user_ids.website_id, self.website_1)

    @users("admin")
    def test_grant_access_sets_partner_website(self):
        """Granting portal access propagates website_id to the partner."""
        wizard = self._open_wizard(self.partner)
        wizard.website_id = self.website_2
        wizard_user = wizard.user_ids
        with patch.object(type(wizard_user), "_send_email", return_value=True):
            wizard_user.action_grant_access()
        self.assertEqual(self.partner.website_id, self.website_2)

    @users("admin")
    def test_grant_access_user_website_id(self):
        """Created portal user inherits website_id via partner's related field."""
        wizard = self._open_wizard(self.partner)
        wizard.website_id = self.website_2
        wizard_user = wizard.user_ids
        with patch.object(type(wizard_user), "_send_email", return_value=True):
            wizard_user.action_grant_access()
        portal_user = self.partner.with_context(active_test=False).user_ids
        self.assertTrue(portal_user)
        self.assertEqual(portal_user.website_id, self.website_2)

    @users("admin")
    def test_invite_again_updates_website(self):
        """Re-inviting an existing portal user updates its website_id."""
        portal_user = mail_new_test_user(
            self.env,
            name="Existing Portal",
            login="existing_portal@example.com",
            email="existing_portal@example.com",
            groups="base.group_portal",
        )
        wizard = self._open_wizard(portal_user.partner_id)
        wizard.website_id = self.website_2
        wizard_user = wizard.user_ids
        with patch.object(type(wizard_user), "_send_email", return_value=True):
            wizard_user.action_invite_again()
        self.assertEqual(portal_user.partner_id.website_id, self.website_2)
        self.assertEqual(portal_user.website_id, self.website_2)
