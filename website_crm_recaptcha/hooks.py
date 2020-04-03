# Copyright 2019 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def uninstall_hook(cr, registry):
    """Unmark crm.lead as recaptcha model."""
    cr.execute(
        """
        UPDATE ir_model
        SET website_form_recaptcha = FALSE
        WHERE model = 'crm.lead'
    """
    )
