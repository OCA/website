{
    "name": "A/B Testing",
    "category": "Website",
    "version": "13.0.1.0.0",
    "author": "Onestein, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://onestein.nl",
    "depends": ["website"],
    "data": [
        "security/ir_model_access.xml",
        "templates/assets.xml",
        "templates/website.xml",
        "views/ir_ui_view_view.xml",
        "views/target_view.xml",
        "views/target_conversion_view.xml",
        "menuitems.xml",
    ],
    "qweb": ["static/src/xml/editor.xml"],
}
