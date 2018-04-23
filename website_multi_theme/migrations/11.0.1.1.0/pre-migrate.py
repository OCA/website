# Copyright 2017 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).


def migrate(cr, version):
    """Restore affected non-qweb views."""
    cr.execute("""
        DELETE FROM ir_ui_view
        WHERE type != 'qweb' AND multi_theme_generated = TRUE
    """)
    cr.execute("""
        UPDATE ir_ui_view
        SET active = TRUE, was_active = FALSE
        WHERE type != 'qweb' AND was_active = TRUE
    """)
