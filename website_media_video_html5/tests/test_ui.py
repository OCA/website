# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged

VIDEO_PATH = "/website_media_video_html5/static/tests/sample.webm"


@tagged("post_install", "-at_install")
class TestUi(HttpCase):
    def test_editor(self):
        self.start_tour("/", "website_media_video_html5_editor", login="admin")

    def test_editor_background(self):
        self.start_tour("/", "website_media_video_html5_background", login="admin")

    def test_public_rendering(self):
        video_url = self.base_url() + VIDEO_PATH
        arch = f"""
            <t t-name="website_media_video_html5.test_page">
                <t t-call="website.layout">
                    <div id="wrap">
                        <section class="o_test_inline">
                            <div class="media_iframe_video"
                                 data-oe-expression="{video_url}?autoplay=1">
                                <div class="css_editable_mode_display"/>
                                <div class="media_iframe_video_size"/>
                            </div>
                        </section>
                        <section class="o_test_background o_background_video"
                                 data-bg-video-src="{video_url}">
                            <div class="container"><p>Hero</p></div>
                        </section>
                        <section class="o_test_youtube">
                            <div class="media_iframe_video"
                                 data-oe-expression="//www.youtube.com/embed/nbso3NVz3p8">
                                <div class="css_editable_mode_display"/>
                                <div class="media_iframe_video_size"/>
                            </div>
                        </section>
                    </div>
                </t>
            </t>
        """
        self.env["website.page"].create(
            {
                "name": "HTML5 video test",
                "url": "/html5-video-test",
                "type": "qweb",
                "arch": arch,
                "is_published": True,
                "website_id": self.env["website"].get_current_website().id,
            }
        )
        self.start_tour("/html5-video-test", "website_media_video_html5_public")
