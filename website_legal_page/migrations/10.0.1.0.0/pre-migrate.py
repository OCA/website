# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(
        env.cr,
        (
            ("website.legal", "website_legal_page.advice"),
            ("website.privacy", "website_legal_page.privacy-policy"),
            ("website.terms", "website_legal_page.terms-of-use"),
        )
    )
