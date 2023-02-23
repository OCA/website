{
    "name": "Website Security",
    "summary": "Creates a group which has access to all website settings",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "version": "16.0.1.0.0",
    "author": "Onestein,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["website"],
    "data": [
        "security/res_groups.xml",
        "security/ir_model_access.xml",
        "security/ir_rule.xml",
        "views/website_config_settings_view.xml",
        "menuitems.xml",
    ],
}
