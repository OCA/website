# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Conditional visibility for internal users in Website",
    "summary": "Only internal users will see the blocks you add this condition to",
    "version": "19.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/website",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["website"],
    "assets": {
        "web.assets_frontend_minimal": [
            "website_conditional_visibility_user_group/static/src/js/inject_dom.esm.js",
        ],
        "web.assets_frontend_lazy": [
            # Remove assets_frontend_minimal
            (
                "remove",
                "website_conditional_visibility_user_group/static/src/js/inject_dom.esm.js",
            ),
        ],
        "web.assets_tests": [
            "website_conditional_visibility_user_group/static/src/tests/*.js"
        ],
        "website.website_builder_assets": [
            "website_conditional_visibility_user_group/static/src/website_builder/**"
        ],
    },
}
