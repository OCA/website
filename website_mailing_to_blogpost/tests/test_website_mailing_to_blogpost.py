# Copyright 2025 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestMassMailing(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blog_id = cls.env.ref("website_blog.blog_blog_1").id
        cls.mailing = cls.env["mailing.mailing"].create(
            {
                "name": "TestMailing",
                "subject": "Test",
                "body_html": '<p>Hello <t t-out="object.name"/></p>',
                "mailing_model_id": cls.env["ir.model"]._get("res.partner").id,
            }
        )

    def test_newsletter_to_blogpost(self):
        newsletter_to_blogpost_wizard_rec = (
            self.env["newsletter.to.blogpost.wizard"]
            .with_context(default_mailing_id=self.mailing.id)
            .create({"blog_id": self.blog_id})
        )
        action = newsletter_to_blogpost_wizard_rec.newsletter_to_blogpost()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertIn(str(self.blog_id), action["url"])
