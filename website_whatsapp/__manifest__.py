# Copyright 2022 WesurRV - Shivam Kachhia <shivamkachhia04@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Whatsapp",
    "summary": "Whatsapp integration",
    "category": "Website",
    "version": "19.0.1.0.0",
    "website": "https://github.com/OCA/website",
    "author": "Shivam-2512, Odoo Community Association (OCA)",
    "maintainers": ["Shivam-2512"],
    "license": "AGPL-3",
    "depends": ["website"],
    "data": [
        "templates/website.xml",
        "views/res_config_settings.xml",
    ],
    "assets": {
        "web.assets_frontend": ["/website_whatsapp/static/src/scss/website.scss"]
    },
    "installable": True,
}
