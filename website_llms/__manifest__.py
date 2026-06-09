{
    "name": "Website llms.txt",
    "version": "16.0.1.0.0",
    "category": "Website",
    "summary": """
        This module adds support for serving a /llms.txt file in the website root.
        The content can be configured per website in the website settings.
    """,
    "website": "https://github.com/OCA/website",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "maintainers": ["marcelsavegnago"],
    "depends": ["website"],
    "data": [
        "views/res_config_settings.xml",
    ],
    "installable": True,
    "application": False,
    "license": "AGPL-3",
}
