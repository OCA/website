# Copyright 2026 Binhex <https://www.binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon

from ..models.website import SITEMAP_DEFAULT_EXCLUDED_PATHS_TEXT


class TestWebsiteExcludeSitemap(BaseCommon):
    def setUp(self):
        super().setUp()
        self.website = self.env["website"].create({"name": "Sitemap Test Website"})

    def _create_cached_sitemap(self):
        sitemap_xml = f"/sitemap-{self.website.id}-test.xml"
        return self.env["ir.attachment"].create(
            {
                "name": sitemap_xml,
                "type": "binary",
                "url": sitemap_xml,
                "raw": b"<xml />",
                "mimetype": "application/xml;charset=utf-8",
            }
        )

    def _create_website_page(self, url="/test-sitemap-page"):
        key_suffix = (url.strip("/") or "home").replace("/", "_").replace("-", "_")
        key = f"website_exclude_sitemap.test_sitemap_page_{key_suffix}"
        view = self.env["ir.ui.view"].create(
            {
                "name": f"Test Sitemap Page {url}",
                "type": "qweb",
                "key": key,
                "arch": (
                    "<t t-name="
                    f"{key}"
                    "<t t-call='website.layout'><div id='wrap'/></t>"
                    "</t>"
                ),
                "website_id": self.website.id,
            }
        )
        return self.env["website.page"].create(
            {
                "url": url,
                "view_id": view.id,
                "website_published": True,
                "website_indexed": True,
            }
        )

    def test_config_settings_updates_website_exclusions(self):
        settings = self.env["res.config.settings"].create(
            {
                "website_id": self.website.id,
                "sitemap_excluded_paths": "/contactus\n/shop*",
            }
        )

        self.assertEqual(
            self.website.sitemap_excluded_paths, settings.sitemap_excluded_paths
        )
        self.assertTrue(self.website._is_sitemap_path_excluded("/contactus"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/shop/category"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/blog"))

    def test_default_exclusions_on_new_website(self):
        website = self.env["website"].create({"name": "Default Sitemap Exclusions"})

        self.assertEqual(
            website.sitemap_excluded_paths, SITEMAP_DEFAULT_EXCLUDED_PATHS_TEXT
        )

    def test_normalize_sitemap_path(self):
        normalize = self.website._normalize_sitemap_path

        self.assertEqual(normalize(None), "/")
        self.assertEqual(normalize("  "), "/")
        self.assertEqual(normalize("/"), "/")
        self.assertEqual(normalize("customers/"), "/customers")
        self.assertEqual(
            normalize("https://www.example.com/blog/example?feed=1"),
            "/blog/example?feed=1",
        )
        self.assertEqual(normalize("https://www.example.com"), "/")

    def test_patterns_without_wildcards_match_exactly(self):
        self.website.sitemap_excluded_paths = "/customers/\n/jobs/apply/\n/profile/"

        self.assertTrue(self.website._is_sitemap_path_excluded("/customers"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/customers/"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/jobs/apply"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/jobs/apply/"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/profile"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/profile/"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/customers/acme"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/customers-other"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/jobs/apply/engineer"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/jobs/application"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/profile/demo"))

    def test_patterns_can_be_separated_by_commas_semicolons_or_newlines(self):
        self.website.sitemap_excluded_paths = (
            "/customers/, /livechat; /blog/*/feed\n/jobs/apply/; /profile/"
        )

        self.assertEqual(
            self.website._get_sitemap_excluded_patterns(),
            [
                "/customers",
                "/livechat",
                "/blog/*/feed",
                "/jobs/apply",
                "/profile",
            ],
        )
        self.assertTrue(self.website._is_sitemap_path_excluded("/customers"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/customers/other"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/livechat"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/blog/other/feed"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/blog/feed/other"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/jobs/apply"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/profile"))

    def test_only_star_is_treated_as_wildcard(self):
        self.website.sitemap_excluded_paths = (
            "/docs?/page\n/category/[abc]\n/files/*/download"
        )

        self.assertTrue(self.website._is_sitemap_path_excluded("/docs?/page"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/docsx/page"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/category/[abc]"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/category/a"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/files/a/download"))
        self.assertFalse(
            self.website._is_sitemap_path_excluded("/files/a/download/extra")
        )

    def test_requirement_default_patterns(self):
        self.website.sitemap_excluded_paths = SITEMAP_DEFAULT_EXCLUDED_PATHS_TEXT

        self.assertTrue(self.website._is_sitemap_path_excluded("/customers"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/customers/acme"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/livechat"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/blog/example/feed"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/blog/feed/example"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/jobs/apply"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/jobs/apply/engineer"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/profile"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/profile/demo"))
        self.assertTrue(self.website._is_sitemap_path_excluded("/website/info"))
        self.assertTrue(
            self.website._is_sitemap_path_excluded("/create-container-error")
        )
        self.assertTrue(self.website._is_sitemap_path_excluded("/machine-creation"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/blog/example-post"))
        self.assertFalse(self.website._is_sitemap_path_excluded("/product/example"))

    def test_write_clears_cached_sitemaps(self):
        attachment = self._create_cached_sitemap()

        self.website.write({"sitemap_excluded_paths": "/contactus"})

        self.assertFalse(attachment.exists())

    def test_reload_sitemap_button_clears_cached_sitemaps(self):
        attachment = self._create_cached_sitemap()
        settings = self.env["res.config.settings"].create(
            {
                "website_id": self.website.id,
            }
        )

        result = settings.action_reload_sitemap()

        self.assertFalse(attachment.exists())
        self.assertEqual(result["tag"], "display_notification")

    def test_website_page_create_clears_cached_sitemaps(self):
        attachment = self._create_cached_sitemap()

        self._create_website_page()

        self.assertFalse(attachment.exists())

    def test_website_page_write_clears_cached_sitemaps(self):
        page = self._create_website_page()
        attachment = self._create_cached_sitemap()

        page.write({"url": "/renamed-sitemap-page"})

        self.assertFalse(attachment.exists())

    def test_website_page_write_only_clears_cached_sitemaps_on_url_change(self):
        page = self._create_website_page()
        attachment = self._create_cached_sitemap()

        page.write({"website_indexed": False})

        self.assertTrue(attachment.exists())

    def test_website_page_unlink_clears_cached_sitemaps(self):
        page = self._create_website_page()
        attachment = self._create_cached_sitemap()

        page.unlink()

        self.assertFalse(attachment.exists())

    def test_enumerate_pages_skips_excluded_urls(self):
        self._create_website_page("/qa-excluded")
        self._create_website_page("/qa-visible")
        self.website.sitemap_excluded_paths = "/qa-excluded"

        pages = self.website.with_context(website_id=self.website.id)._enumerate_pages(
            force=True
        )
        locs = {page["loc"] for page in pages}

        self.assertNotIn("/qa-excluded", locs)
        self.assertIn("/qa-visible", locs)
