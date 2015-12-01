# -*- coding: utf-8 -*-
# License AGPL-3: Antiun Ingenieria S.L. - Antonio Espinosa
# See README.rst file on addon root folder for more details


def migrate(cr, version):
    # Copy res.company.website_logo_to_be_delete to
    #   first website.logo to that company
    cr.execute("""
        SELECT c.id, c.website_logo_to_be_delete
          FROM res_company c
    """)
    companies = cr.fetchall()
    for company in companies:
        if not company[1]:
            continue
        cr.execute("""
            SELECT w.id, w.company_id
              FROM website w
             WHERE w.company_id = %d
        """ % company[0])
        web = cr.fetchone()
        if web:
            cr.execute("""
                UPDATE website
                   SET logo = '%s'
                 WHERE id = %d
            """ % (company[1], web[0]))

    # Delete column res.company.website_logo_to_be_delete
    cr.execute("""
        ALTER TABLE res_company
        DROP COLUMN website_logo_to_be_delete
    """)
