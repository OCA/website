# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Mobile Button",
    "summary": """Add a mobile button box for easier configuration""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "depends": ["website"],
    "data": ["views/templates.xml"],
    "assets": {
        "web.assets_frontend": [
            "website_mobile_button/static/src/scss/*.scss",
        ],
    },
    "demo": [],
}
