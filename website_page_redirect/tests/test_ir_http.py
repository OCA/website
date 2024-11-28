# Copyright 2024 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import http
from odoo.tests import HOST, HttpCase, Opener, get_db_name, new_test_user


class TestIrHttp(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.website = cls.env["website"].sudo().get_current_website()
        cls.website_designer = new_test_user(
            cls.env,
            "website_designer",
            groups="base.group_user,website.group_website_designer",
        )

    def setUp(self):
        super().setUp()
        self.session = http.root.session_store.new()
        self.session.update(http.get_default_session(), db=get_db_name())
        self.opener = Opener(self.env.cr)
        self.opener.cookies.set("session_id", self.session.sid, domain=HOST, path="/")

    def test_404(self):
        redirect_response = self.url_open(
            "/non-existing-page",
            allow_redirects=False,
        )
        self.assertEqual(redirect_response.status_code, 404)

    def test_http_redirect(self):
        http_redirect_page = self.env["website.page"].create(
            {
                "website_id": self.website.id,
                "name": "http-redirect",
                "url": "/http-redirect",
                "type": "qweb",
                "arch": "<t t-call='website.layout'>http-redirect</t>",
                "is_published": True,
                "is_redirect": True,
                "redirect_method": "http",
                "redirect_http_code": "301",
                "redirect_url": "https://corporatehub.eu",
            }
        )

        redirect_response = self.url_open(
            http_redirect_page.url,
            allow_redirects=False,
        )

        self.assertEqual(redirect_response.status_code, 301)
        self.assertEqual(
            "https://corporatehub.eu",
            redirect_response.headers["Location"],
        )

    def test_no_http_redirect_for_website_designer(self):
        http_redirect_page = self.env["website.page"].create(
            {
                "website_id": self.website.id,
                "name": "http-redirect",
                "url": "/http-redirect",
                "type": "qweb",
                "arch": "<t t-call='website.layout'>http-redirect</t>",
                "is_published": True,
                "is_redirect": True,
                "redirect_method": "http",
                "redirect_http_code": "301",
                "redirect_url": "https://corporatehub.eu",
            }
        )

        login_response = self.url_open(
            "/web/login",
            data={
                "login": self.website_designer.login,
                "password": self.website_designer.login,
                "csrf_token": http.Request.csrf_token(self),
            },
        )
        login_response.raise_for_status()

        redirect_response = self.url_open(
            http_redirect_page.url,
            allow_redirects=False,
        )

        self.assertEqual(redirect_response.status_code, 200)

    def test_meta_redirect(self):
        http_redirect_page = self.env["website.page"].create(
            {
                "website_id": self.website.id,
                "name": "meta-redirect",
                "url": "/meta-redirect",
                "type": "qweb",
                "arch": "<t t-call='website.layout'>meta-redirect</t>",
                "is_published": True,
                "is_redirect": True,
                "redirect_method": "meta",
                "redirect_delay": 5,
                "redirect_url": "https://corporatehub.eu",
            }
        )

        redirect_response = self.url_open(http_redirect_page.url)

        self.assertEqual(redirect_response.status_code, 200)
        self.assertIn(
            (
                "<meta"
                ' http-equiv="refresh"'
                ' content="5;url=https://corporatehub.eu"/>'
            ),
            redirect_response.content.decode("utf-8"),
        )

    def test_no_meta_redirect_for_website_designer(self):
        http_redirect_page = self.env["website.page"].create(
            {
                "website_id": self.website.id,
                "name": "meta-redirect",
                "url": "/meta-redirect",
                "type": "qweb",
                "arch": "<t t-call='website.layout'>meta-redirect</t>",
                "is_published": True,
                "is_redirect": True,
                "redirect_method": "meta",
                "redirect_delay": 5,
                "redirect_url": "https://corporatehub.eu",
            }
        )

        login_response = self.url_open(
            "/web/login",
            data={
                "login": self.website_designer.login,
                "password": self.website_designer.login,
                "csrf_token": http.Request.csrf_token(self),
            },
        )
        login_response.raise_for_status()

        redirect_response = self.url_open(http_redirect_page.url)

        self.assertEqual(redirect_response.status_code, 200)
        self.assertNotIn(
            (
                "<meta"
                ' http-equiv="refresh"'
                ' content="5;url=https://corporatehub.eu"/>'
            ),
            redirect_response.content.decode("utf-8"),
        )

    def test_js_href_redirect(self):
        http_redirect_page = self.env["website.page"].create(
            {
                "website_id": self.website.id,
                "name": "js-href-redirect",
                "url": "/js-href-redirect",
                "type": "qweb",
                "arch": "<t t-call='website.layout'>js-href-redirect</t>",
                "is_published": True,
                "is_redirect": True,
                "redirect_method": "js-href",
                "redirect_delay": 5,
                "redirect_url": "https://corporatehub.eu",
            }
        )

        redirect_response = self.url_open(http_redirect_page.url)

        self.assertEqual(redirect_response.status_code, 200)
        self.assertIn(
            (
                "setTimeout(\n"
                "    function() {"
                " window.location.href = 'https://corporatehub.eu'; },\n"
                "    5000,\n"
                ");"
            ),
            redirect_response.content.decode("utf-8"),
        )

    def test_no_js_href_redirect_for_website_designer(self):
        http_redirect_page = self.env["website.page"].create(
            {
                "website_id": self.website.id,
                "name": "js-href-redirect",
                "url": "/js-href-redirect",
                "type": "qweb",
                "arch": "<t t-call='website.layout'>js-href-redirect</t>",
                "is_published": True,
                "is_redirect": True,
                "redirect_method": "js-href",
                "redirect_delay": 5,
                "redirect_url": "https://corporatehub.eu",
            }
        )

        login_response = self.url_open(
            "/web/login",
            data={
                "login": self.website_designer.login,
                "password": self.website_designer.login,
                "csrf_token": http.Request.csrf_token(self),
            },
        )
        login_response.raise_for_status()

        redirect_response = self.url_open(http_redirect_page.url)

        self.assertEqual(redirect_response.status_code, 200)
        self.assertNotIn(
            (
                "setTimeout(\n"
                "    function() {"
                " window.location.href = 'https://corporatehub.eu'; },\n"
                "    5000,\n"
                ");"
            ),
            redirect_response.content.decode("utf-8"),
        )

    def test_js_replace_redirect(self):
        http_redirect_page = self.env["website.page"].create(
            {
                "website_id": self.website.id,
                "name": "js-replace-redirect",
                "url": "/js-replace-redirect",
                "type": "qweb",
                "arch": "<t t-call='website.layout'>js-replace-redirect</t>",
                "is_published": True,
                "is_redirect": True,
                "redirect_method": "js-replace",
                "redirect_delay": 5,
                "redirect_url": "https://corporatehub.eu",
            }
        )

        redirect_response = self.url_open(http_redirect_page.url)

        self.assertEqual(redirect_response.status_code, 200)
        self.assertIn(
            (
                "setTimeout(\n"
                "    function() {"
                " window.location.replace('https://corporatehub.eu'); },\n"
                "    5000,\n"
                ");"
            ),
            redirect_response.content.decode("utf-8"),
        )

    def test_no_js_replace_redirect_for_website_designer(self):
        http_redirect_page = self.env["website.page"].create(
            {
                "website_id": self.website.id,
                "name": "js-replace-redirect",
                "url": "/js-replace-redirect",
                "type": "qweb",
                "arch": "<t t-call='website.layout'>js-replace-redirect</t>",
                "is_published": True,
                "is_redirect": True,
                "redirect_method": "js-replace",
                "redirect_delay": 5,
                "redirect_url": "https://corporatehub.eu",
            }
        )

        login_response = self.url_open(
            "/web/login",
            data={
                "login": self.website_designer.login,
                "password": self.website_designer.login,
                "csrf_token": http.Request.csrf_token(self),
            },
        )
        login_response.raise_for_status()

        redirect_response = self.url_open(http_redirect_page.url)

        self.assertEqual(redirect_response.status_code, 200)
        self.assertNotIn(
            (
                "setTimeout(\n"
                "    function() {"
                " window.location.replace('https://corporatehub.eu'); },\n"
                "    5000,\n"
                ");"
            ),
            redirect_response.content.decode("utf-8"),
        )
