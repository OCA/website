# Copyright 2020 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    # The template is noupdate=1; force lang update
    template = env.ref("website_crm_quick_answer.email_template")
    if template.lang == '${object.env.context.get("lang")}':
        template.lang = (
            '${object.env.context.get("lang") or '
            "object.partner_id.lang or object.company_id.lang or "
            "object.env.user.lang}"
        )
