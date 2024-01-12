# SPDX-FileCopyrightText: 2010-2014 Elico Corp
# SPDX-FileContributor: Augustin Cisterne-Kaas <augustin.cisterne-kaas@elico-corp.com>
# SPDX-FileCopyrightText: 2015 Tech-Receptives Solutions Pvt. Ltd.
# SPDX-FileCopyrightText: 2019 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Website reCAPTCHA v2",
    "version": "12.0.0.0.1",
    "category": "Website",
    "depends": ["website"],
    "author": (
        "Elico Corp, Tech Receptives, Coop IT Easy SC, "
        "Odoo Community Association (OCA)"
    ),
    "license": "AGPL-3",
    "website": "https://github.com/OCA/website",
    "summary": "Add google recaptcha to forms.",
    "data": ["views/website_view.xml", "views/res_config.xml"],
    "installable": True,
}
