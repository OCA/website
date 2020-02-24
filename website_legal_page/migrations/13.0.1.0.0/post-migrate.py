# Copyright 2020 Alexandre Díaz - Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade  # pylint: disable=W7936

from odoo.addons.website_legal_page import _merge_views

OLD_VIEW_XML_IDS = [
    "website_legal_page.advice",
    "website_legal_page.privacy-policy",
    "website_legal_page.terms-of-use",
    "website_sale.terms",
]


def _disable_old_views(env, xmlids):
    # Search and deactivate views
    old_view_ids = env["ir.ui.view"].search(
        [("key", "in", xmlids), ("active", "=", True)]
    )
    old_view_ids.write({"active": False})
    # Unpublish related website pages
    env["website.page"].search(
        [("view_id", "in", old_view_ids.ids), ("is_published", "=", True)]
    ).write({"is_published": False})


@openupgrade.migrate()
def migrate(env, version):
    _merge_views(env, OLD_VIEW_XML_IDS)
    _disable_old_views(env, OLD_VIEW_XML_IDS)
