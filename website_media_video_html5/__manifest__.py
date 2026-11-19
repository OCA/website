# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Media Video HTML5",
    "summary": "Embed self-hosted and CDN video files in website pages",
    "version": "19.0.1.0.0",
    "category": "Website",
    "author": "bosd, Odoo Community Association (OCA)",
    "maintainers": ["bosd"],
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "depends": ["website"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "html_editor.assets_media_dialog": [
            "website_media_video_html5/static/src/js/html5_video_utils.esm.js",
            "website_media_video_html5/static/src/editor/video_selector.esm.js",
            "website_media_video_html5/static/src/editor/video_selector.xml",
        ],
        "html_editor.assets_editor": [
            "website_media_video_html5/static/src/editor/media_plugin.esm.js",
        ],
        "web.assets_frontend": [
            "website_media_video_html5/static/src/js/html5_video_utils.esm.js",
            "website_media_video_html5/static/src/js/media_video.esm.js",
            "website_media_video_html5/static/src/js/background_video.esm.js",
            "website_media_video_html5/static/src/scss/html5_video.scss",
        ],
        "web.assets_tests": [
            "website_media_video_html5/static/tests/tours/**/*",
        ],
    },
    "installable": True,
}
