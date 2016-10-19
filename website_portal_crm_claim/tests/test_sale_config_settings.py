# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.tests.common import TransactionCase


class SaleConfigSettingsCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(SaleConfigSettingsCase, self).setUp(*args, **kwargs)
        self.claim_alias = self.env.ref(
            "website_portal_crm_claim.mail_alias_claim")
        self.crm_claim = self.env.ref("crm_claim.model_crm_claim")

    def wizard(self):
        return self.env["sale.config.settings"].create({})

    def new_alias(self):
        return self.env["mail.alias"].create({
            "alias_model_id": self.crm_claim.id,
            "alias_name": "aaaa",
            "alias_contact": "everyone",
        })

    def test_bundled_alias(self):
        """If the bundled alias exists, it is preferred."""
        self.new_alias()
        wizard = self.wizard()
        self.assertEqual(
            self.claim_alias, wizard._find_default_claim_alias_id())
        self.assertEqual("claims", wizard.alias_claim)

    def test_user_defined_alias(self):
        """The bundled alias was deleted, the user created another one."""
        self.claim_alias.unlink()
        new_alias, wizard = self.new_alias(), self.wizard()
        self.assertEqual(
            new_alias, wizard._find_default_claim_alias_id())
        self.assertEqual("aaaa", wizard.alias_claim)

    def test_no_alias_creates_one(self):
        """No alias is found, we create one automatically."""
        self.claim_alias.unlink()
        wizard = self.wizard()
        self.assertEqual("claims", wizard.alias_claim)

    def test_alias_updated(self):
        """Alias gets correctly updated."""
        wizard = self.wizard()
        wizard.alias_claim = "aaaa"
        wizard.execute()
        self.assertEqual(self.claim_alias.alias_name, "aaaa")
