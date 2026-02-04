# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)
from lxml import etree

from odoo import exceptions
from odoo.tests.common import Form, TransactionCase


class TestWebEditorCleanUrl(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Configuration = cls.env["web.editor.clean.url.configuration"]
        Configuration.search([]).active = False
        cls.config = Configuration.create(
            {
                "hostname": "admafia.com",
                "remove_query_parameter": "set,__cft__%5B0%5D,__tn__",
            }
        )
        cls.test_url = (
            "https://www.admafia.com/photo/?fbid=42&set=a&__cft__%5B0%5D=b&__tn__=c"
        )
        cls.test_url_escaped = (
            "https://www.admafia.com/photo/?fbid=42&amp;set=a&amp;__cft__%5B0%5D=b"
            "&amp;__tn__=c"
        )
        cls.cleaned_test_url = "https://www.admafia.com/photo/?fbid=42"

    def test_preview(self):
        with Form(self.config) as form:
            form.test_url = self.test_url
            self.assertEqual(form.preview_url, self.cleaned_test_url)

    def test_failure(self):
        with self.assertRaises(exceptions.ValidationError), Form(self.config) as form:
            form.replace_regex = "?"
        with self.assertRaises(exceptions.ValidationError), Form(self.config) as form:
            form.replace_regex = "?"
            form.test_url = "https://www.admafia.com/?debug"

    def test_apply_all(self):
        view = self.env["ir.ui.view"].create(
            {
                "type": "qweb",
                "arch_db": self.env["ir.qweb"]._render(
                    etree.fromstring(
                        "<div>"
                        '<div><a t-att-href="test_url">link</a></div>'
                        '<div><a href="http://admafia2.com">not replaced</a></div>'
                        '<div><a href="#anchor">ignored</a></div>'
                        '<div><a id="anchor">ignored</a></div>'
                        "</div>"
                    ),
                    {"test_url": self.test_url},
                ),
            }
        )
        self.config.apply_all()
        self.assertNotIn(self.test_url_escaped, view.arch_db)
        self.assertIn(self.cleaned_test_url, view.arch_db)
        self.assertIn('<a href="#anchor">', view.arch_db)
        self.assertIn('<a href="http://admafia2.com">', view.arch_db)
        self.assertIn(self.test_url_escaped, view.arch_prev)

    def test_replacement(self):
        self.env["web.editor.clean.url.configuration"].create({})
        view = self.env["ir.ui.view"].create(
            {
                "type": "qweb",
                "arch_db": "<div />",
            }
        )
        view.save(
            f'<div><a href="{self.test_url}">link</a></div>',
            xpath=".",
        )
        self.assertNotIn(self.test_url_escaped, view.arch_db)
        self.assertIn(self.cleaned_test_url, view.arch_db)

    def test_regex(self):
        config = self.config
        config.remove_query_parameter = False
        config.replace_regex = r"\?fbid=([^&]+).*$"
        config.replace_regex_sub = r"?fbid=\1"
        config.test_url = self.test_url
        self.assertEqual(config.preview_url, self.cleaned_test_url)

    def test_idempotence(self):
        apply_all_records = [
            records
            for records, _dummy in self.config._apply_all_get_records_and_field()
        ]
        all_views = sum(
            [records for records in apply_all_records if records._name == "ir.ui.view"],
            self.env["ir.ui.view"],
        )
        all_views.write(
            {
                "arch_prev": False,
            }
        )
        self.config.apply_all()
        self.assertFalse(any(all_views.mapped("arch_prev")))
