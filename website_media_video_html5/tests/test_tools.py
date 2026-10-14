# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged

from ..tools import (
    ALLOWED_HOSTS_PARAM,
    get_allowed_hosts,
    get_html5_video_mimetype,
    get_html5_video_url_data,
    is_html5_video_url,
    split_video_url,
)

CDN = "res.cloudinary.com"
CDN_URL = (
    "https://res.cloudinary.com/demo/video/upload/f_auto:video,q_auto/v1/videos/abc"
)


@tagged("post_install", "-at_install")
class TestTools(TransactionCase):
    def test_is_html5_video_url_by_extension(self):
        for url in (
            "https://cdn.example.com/media/video.mp4",
            "http://cdn.example.com/media/VIDEO.MP4",
            "//cdn.example.com/video.webm",
            "https://cdn.example.com/video.ogv?token=abc",
            "https://cdn.example.com/video.m4v#t=10",
        ):
            with self.subTest(url=url):
                self.assertTrue(is_html5_video_url(url))

    def test_is_not_html5_video_url(self):
        for url in (
            False,
            "",
            "https://cdn.example.com/page.html",
            "https://cdn.example.com/video.mp4.html",
            "cdn.example.com/video.mp4",
            "javascript:alert(1)//video.mp4",
            "ftp://cdn.example.com/video.mp4",
            "data:video/mp4;base64,AAAA",
            CDN_URL,
        ):
            with self.subTest(url=url):
                self.assertFalse(is_html5_video_url(url))

    def test_is_html5_video_url_allowed_host(self):
        self.assertTrue(is_html5_video_url(CDN_URL, [CDN]))
        self.assertTrue(
            is_html5_video_url("https://eu.res.cloudinary.com/video/abc", [CDN])
        )
        self.assertFalse(
            is_html5_video_url("https://fakeres.cloudinary.com.evil.com/x", [CDN])
        )
        self.assertFalse(is_html5_video_url("https://example.com/abc", [CDN]))

    def test_get_allowed_hosts(self):
        self.env["ir.config_parameter"].set_param(
            ALLOWED_HOSTS_PARAM, " res.cloudinary.com,\nWWW.Cdn.Example.com ,, "
        )
        self.assertEqual(
            get_allowed_hosts(self.env), ["res.cloudinary.com", "cdn.example.com"]
        )
        self.env["ir.config_parameter"].set_param(ALLOWED_HOSTS_PARAM, False)
        self.assertEqual(get_allowed_hosts(self.env), [])

    def test_mimetype(self):
        self.assertEqual(
            get_html5_video_mimetype("https://x.org/a.mp4?b=c"), "video/mp4"
        )
        self.assertEqual(get_html5_video_mimetype("https://x.org/a.WEBM"), "video/webm")
        self.assertEqual(get_html5_video_mimetype("https://x.org/a.ogv"), "video/ogg")
        self.assertIsNone(get_html5_video_mimetype(CDN_URL))

    def test_split_video_url(self):
        self.assertEqual(
            split_video_url("https://x.org/a.mp4?sig=a%2Fb&autoplay=1&loop=1#t=5"),
            ("https://x.org/a.mp4?sig=a%2Fb#t=5", {"autoplay": True, "loop": True}),
        )
        self.assertEqual(
            split_video_url("https://x.org/a.mp4?controls=0"),
            ("https://x.org/a.mp4", {"hide_controls": True}),
        )
        # Only our exact pairs are options.
        self.assertEqual(
            split_video_url("https://x.org/a.mp4?autoplay=0&loop=true"),
            ("https://x.org/a.mp4?autoplay=0&loop=true", {}),
        )

    def test_get_html5_video_url_data(self):
        self.assertIsNone(get_html5_video_url_data("https://youtu.be/nbso3NVz3p8"))
        self.assertEqual(
            get_html5_video_url_data("https://cdn.example.com/video.mp4"),
            {
                "platform": "html5",
                "embed_url": "//cdn.example.com/video.mp4",
                "video_id": False,
                "params": {},
            },
        )

    def test_get_html5_video_url_data_options(self):
        data = get_html5_video_url_data(
            "https://cdn.example.com/video.mp4?sig=x&autoplay=1&controls=0#t=3",
            autoplay=True,
            loop=True,
            hide_controls=False,
            start_from="42",
        )
        self.assertEqual(
            data["embed_url"],
            "//cdn.example.com/video.mp4?sig=x&autoplay=1&loop=1#t=42",
        )
        self.assertEqual(data["params"], {"autoplay": 1, "loop": 1})
        data = get_html5_video_url_data(
            "//cdn.example.com/video.mp4", hide_controls=True, start_from="00:00"
        )
        self.assertEqual(data["embed_url"], "//cdn.example.com/video.mp4?controls=0")
        data = get_html5_video_url_data(CDN_URL, [CDN], start_from="7s")
        self.assertEqual(data["embed_url"], CDN_URL.removeprefix("https:") + "#t=7")
