# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # We're adding cookiebot_enabled to the website so it's easier to disable the
    # cookiebot scripts temporarily
    env["website"].search([("cookiebot_dgid", "!=", False)]).cookiebot_enabled = True
