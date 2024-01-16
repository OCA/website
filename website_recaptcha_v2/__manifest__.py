# SPDX-FileCopyrightText: 2010-2014 Elico Corp
# SPDX-FileContributor: Augustin Cisterne-Kaas <augustin.cisterne-kaas@elico-corp.com>
# SPDX-FileCopyrightText: 2015 Tech-Receptives Solutions Pvt. Ltd.
# SPDX-FileCopyrightText: 2019 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Website reCAPTCHA v2",
    "version": "16.0.1.0.0",
    "category": "Website",
    "depends": ["website"],
    "author": (
        "Elico Corp, Tech Receptives, Coop IT Easy SC, "
        "Odoo Community Association (OCA)"
    ),
    "license": "AGPL-3",
    "website": "https://github.com/OCA/website",
    "summary": "Helper module to add reCAPTCHA v2 to website forms",
    "data": [
        "views/res_config_settings_view.xml",
        "views/website_templates.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
}
