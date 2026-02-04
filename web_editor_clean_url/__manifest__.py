# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Clean URLs in website editor",
    "summary": "Remove tracking, ephemeral and similar parameters from URLs",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Website/Website",
    "website": "https://github.com/OCA/website",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "AGPL-3",
    "depends": [
        "website",
    ],
    "data": [
        "data/ir_actions_server.xml",
        "data/web_editor_clean_url_configuration.xml",
        "security/ir.model.access.csv",
        "views/web_editor_clean_url_configuration.xml",
        "views/menu.xml",
    ],
}
