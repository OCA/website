# Copyright 2018 Simone Orsi <simone.orsi@camptocamp.com>
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase
from odoo.modules.module import get_resource_path
from odoo import tools
from lxml.html import document_fromstring


def load_xml(cr, module, filepath, kind='demo'):
    tools.convert_file(
        cr, module,
        get_resource_path(module, filepath),
        {}, mode='init', noupdate=False, kind=kind)


class UICase(HttpCase):
    def setUp(self):
        super(UICase, self).setUp()
        self._reload_page()
        self.website = self.env['website'].browse(1)
        self.domain = self.website._get_canonical_domain()
        self.path = "/canonical-demo"
        self.url_absolute = self.domain + self.path
        self.qstring = "?ultimate_answer=42"
        self.url_full = "%s%s" % (self.url_absolute, self.qstring)
        self.url_data = self.url_open(self.url_full)
        self.doc = document_fromstring(self.url_data.content)

    def _reload_page(self):
        # if you run tests more than once (locally for instance)
        # if you update the page we make sure is reloaded.
        self.env.ref('website_canonical_url.canonical_demo_view').unlink()
        load_xml(self.cr, 'website_canonical_url', 'demo/pages.xml')

    def test_canonical(self):
        """Canonical URL is built OK."""
        node = self.doc.xpath("/html/head/link[@rel='canonical']")[0]
        self.assertEqual(node.attrib["href"], self.url_absolute)

    def test_pager_next(self):
        """Next pager link is OK."""
        node = self.doc.xpath("/html/head/link[@rel='next']")[0]
        self.assertEqual(
            node.attrib["href"],
            "%s/page/3%s" % (self.path, self.qstring),
        )

    def test_pager_prev(self):
        """Prev pager link is OK."""
        node = self.doc.xpath("/html/head/link[@rel='prev']")[0]
        self.assertEqual(
            node.attrib["href"],
            "%s%s" % (self.path, self.qstring),
        )
