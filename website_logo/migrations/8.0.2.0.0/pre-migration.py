# -*- coding: utf-8 -*-
# License AGPL-3: Antiun Ingenieria S.L. - Antonio Espinosa
# See README.rst file on addon root folder for more details


def migrate(cr, version):
    # Rename res.company.website_logo to res.company.website_logo_to_be_delete
    cr.execute("""
        ALTER TABLE res_company
        RENAME COLUMN website_logo TO website_logo_to_be_delete
    """)
