# -*- coding: utf-8 -*-
# Copyright 2018 Wolfgang Pichler, Callino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product SEO",
    "summary": "Does better integrate SEO Redirection with products",
    "version": "10.0.1.0.0",
    # see https://odoo-community.org/page/development-status
    "development_status": "Production/Stable",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "Wolfgang Pichler <wpichler@callino.at>, "
              "Odoo Community Association (OCA)",
    # see https://odoo-community.org/page/maintainer-role for a description 
    # of the maintainer role and responsibilities
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_seo_redirection", "website_sale"
    ],
}
