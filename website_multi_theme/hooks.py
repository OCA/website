# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, SUPERUSER_ID


def uninstall_hook(cr, registry):
    """Loaded before uninstalling the module.
    Reset active field to original value saved in was_active field
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    domain = [('multitheme_copy_ids', '!=', False)]
    for value in (True, False):
        env['ir.ui.view']\
            .with_context(active_test=False)\
            .search(domain + [('was_active', '=', value)])\
            .write({
                'active': value,
            })
