# Copyright 2019 Jairo Llopis - Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """Move global ``ir.config_parameter`` keys to website."""
    ICP = env["ir.config_parameter"]
    websites = env["website"].search([
        ("recaptcha_key_site", "=", False),
        ("recaptcha_key_secret", "=", False),
    ])
    site = ICP.get_param("recaptcha.key.site")
    secret = ICP.get_param("recaptcha.key.secret")
    if site and secret:
        websites.write({
            "recaptcha_key_site": site,
            "recaptcha_key_secret": secret,
        })
    ICP.set_param("recaptcha.key.site", False)
    ICP.set_param("recaptcha.key.secret", False)
