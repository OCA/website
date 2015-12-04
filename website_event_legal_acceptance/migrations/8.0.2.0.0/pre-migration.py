# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    # Fill legal terms table
    cr.execute("""
        INSERT INTO website_sale_product_legal_legal_term(id, name, contents)
        SELECT id, name, description
        FROM event_legal_template
    """)

    # Fill event and legal terms relation
    cr.execute("""
        INSERT INTO website_event_sale_legal_term_event_rel(
            event_event_id,
            website_sale_product_legal_legal_term_id)
        SELECT id, legal_acceptance
        FROM event_event
        WHERE legal_acceptance IS NOT NULL
    """)
