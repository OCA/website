# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    # Get automated action's ID
    cr.execute("""
        SELECT id FROM ir_model_data
        WHERE module = 'website_crm_quick_answer' AND name = 'automated_action'
    """)
    # Remove its filter_id, now that it is replaced with filter_domain
    cr.execute(
        "UPDATE base_action_rule SET filter_id = NULL WHERE id = %s",
        (cr.fetchone()[0],))
