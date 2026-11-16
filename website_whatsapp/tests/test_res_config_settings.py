# Copyright 2025 Studio73 - Eugenio Micó <eugenio@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestResConfigSettings(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].create({"name": "Test Website"})
        cls.config = cls.env["res.config.settings"].create(
            {
                "website_id": cls.website.id,
            }
        )

    def test_compute_whatsapp_enabled(self):
        self.assertFalse(self.config.whatsapp_enabled)
        self.config.website_id.update({"whatsapp_number": "123456789"})
        self.config.invalidate_recordset()
        self.assertTrue(self.config.whatsapp_enabled)
        self.website.update({"whatsapp_number": False})
        self.config.invalidate_recordset()
        self.assertFalse(self.config.whatsapp_enabled)

    def test_inverse_whatsapp_enabled(self):
        self.website.invalidate_recordset()
        self.config.invalidate_recordset()
        self.config.whatsapp_enabled = False
        self.assertFalse(self.website.whatsapp_number)
