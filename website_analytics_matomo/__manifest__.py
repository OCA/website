# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Matomo Analytics",
    "category": "Website",
    "summary": """Module add Matomo Tracking Code JS script on all the website pages.""",
    "version": "15.0.1.0.0",
    "author": "Nitrokey GmbH, Odoo Community Association (OCA),",
    "website": "https://github.com/OCA/website",
    "license": "LGPL-3",
    "depends": [
        "website",
    ],
    "data": [
        "views/website.xml",
        "views/website_config_settings.xml",
        "templates/website.xml",
    ],
    "installable": True,
    "application": False,
}
