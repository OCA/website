# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Rename the auto-generated XML-ID for the old ir.actions.server record, which is
    # now explicit in data
    mod = "website_crm_quick_answer"
    openupgrade.rename_xmlids(
        env.cr,
        [(f"{mod}.automated_action_ir_actions_server", f"{mod}.send_email_action")],
    )
