# Copyright 2020 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openupgradelib import openupgrade as ou
from openupgradelib.openupgrade_tools import (
    convert_html_fragment,
    convert_html_replacement_class_shortcut as _r,
)

REPLACEMENTS = (
    _r(
        # Use XPath mode because LXML's CSS mode doesn't support `:has()`
        selector="""
        //*
        [hasclass('form-field', 'o_required')]
        [//input[not(@required)]]
        """,
        selector_mode="xpath",
        class_rm="o_required",
    ),
)


@ou.migrate()
def migrate(env, version):
    """Fix existing form that lost their required behavior.

    Setting fields to required might break existing functionality that passed
    unnoticed thanks to the bug fixed in this version, so the fix is not
    requiring the fields, but making them as not required.
    """
    candidates = env['ir.ui.view'].search([
        ("type", "=", "qweb"),
        ("arch_db", "like", "o_required"),
    ])
    for view in candidates:
        old_arch = view.arch
        new_arch = convert_html_fragment(old_arch, REPLACEMENTS)
        if old_arch != new_arch:
            view.arch = new_arch
