# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged

from ..tools import ALLOWED_HOSTS_PARAM


@tagged("post_install", "-at_install")
class TestVideoUrlData(HttpCase):
    def setUp(self):
        super().setUp()
        self.authenticate("admin", "admin")

    def _video_url_data(self, video_url, **options):
        return self.make_jsonrpc_request(
            "/html_editor/video_url/data", {"video_url": video_url, **options}
        )

    def test_video_file(self):
        res = self._video_url_data(
            "https://cdn.example.com/video.mp4", autoplay=True, start_from="10"
        )
        self.assertEqual(res["platform"], "html5")
        self.assertEqual(
            res["embed_url"], "//cdn.example.com/video.mp4?autoplay=1#t=10"
        )

    def test_allowed_host(self):
        url = "https://res.cloudinary.com/demo/video/upload/v1/videos/abc"
        self.assertTrue(self._video_url_data(url)["error"])
        self.env["ir.config_parameter"].set_param(
            ALLOWED_HOSTS_PARAM, "res.cloudinary.com"
        )
        res = self._video_url_data(url)
        self.assertEqual(res["platform"], "html5")
        self.assertEqual(res["embed_url"], url.removeprefix("https:"))

    def test_other_platforms_unchanged(self):
        res = self._video_url_data("https://youtu.be/nbso3NVz3p8")
        self.assertEqual(res["platform"], "youtube")
        self.assertEqual(res["video_id"], "nbso3NVz3p8")

    def test_invalid_url(self):
        res = self._video_url_data("https://www.example.com/page.html")
        self.assertTrue(res["error"])

    def test_settings(self):
        settings = self.env["res.config.settings"].create(
            {"html5_video_allowed_hosts": "res.cloudinary.com"}
        )
        settings.execute()
        self.assertEqual(
            self.env["ir.config_parameter"].get_param(ALLOWED_HOSTS_PARAM),
            "res.cloudinary.com",
        )
