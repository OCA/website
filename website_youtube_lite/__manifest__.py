# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Youtube Lite Style",
    "summary": """This module allows to use youtube-lite tag""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "depends": ["website"],
    "assets": {
        "web.assets_frontend": [
            "website_youtube_lite/static/src/js/lite-yt-embed.js",
            "website_youtube_lite/static/src/css/lite-yt-embed.css",
        ]
    },
}
