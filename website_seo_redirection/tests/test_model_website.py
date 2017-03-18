# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import json
import logging
from urllib2 import BaseHandler

from odoo.tests.common import HttpCase
_logger = logging.getLogger(__name__)


# HACK http://stackoverflow.com/a/39248995/1468388
class ChangeTypeProcessor(BaseHandler):
    def http_request(self, req):
        req.unredirected_hdrs["Content-type"] = "application/json"
        return req


class WebsiteCase(HttpCase):
    def search_page(self, query):
        """Perform a page search using JSON-RPC.

        You need all this stuff to get a bound request.
        """
        self.authenticate("admin", "admin")
        self.opener.add_handler(ChangeTypeProcessor())
        params = {
            "id": None,
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "website",
                "method": "search_pages",
                "args": [
                    self.env["website"]._get_current_website_id("localhost"),
                    query,
                ],
            }
        }
        response = json.load(
            self.url_open("/web/dataset/call", json.dumps(params)))
        _logger.info("JSON Response:\n%s", response)
        result = [page["loc"] for page in response["result"]]
        _logger.info("URLs found:\n%s", result)
        return result

    def test_url_found_no_query(self):
        """``/seo/sample`` should be found."""
        found = self.search_page("")
        self.assertIn("/seo/sample", found)
        self.assertIn("/seo/sample/no-relocate", found)
        self.assertIn("/page/website_seo_redirection.sample_page", found)
        self.assertEqual(len(found), len(set(found)))

    def test_url_found_queried_good(self):
        """``/seo/sample`` should be found."""
        found = self.search_page("sample")
        self.assertIn("/seo/sample", found)
        self.assertIn("/seo/sample/no-relocate", found)
        self.assertIn("/page/website_seo_redirection.sample_page", found)
        self.assertEqual(len(found), len(set(found)))

    def test_url_found_queried_bad(self):
        """``/seo/sample`` should not be found."""
        found = self.search_page("trololo")
        self.assertNotIn("/seo/sample", found)
        self.assertNotIn("/seo/sample/no-relocate", found)
        self.assertNotIn("/page/website_seo_redirection.sample_page", found)
        self.assertEqual(len(found), len(set(found)))
