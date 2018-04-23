# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import logging


from odoo import api, SUPERUSER_ID


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    # migrate multi_theme_generated to origin_view_id
    cr.execute("""SELECT id FROM ir_ui_view
    WHERE multi_theme_generated_tmp IS TRUE""")
    ids = [result[0] for result in cr.fetchall()]
    _logger.debug('Views with multi_theme_generated: %s', ids)

    env = api.Environment(cr, SUPERUSER_ID, {})

    for view in env['ir.ui.view'].browse(ids):
        # extract origin_view_id from name field
        # which has one of following pattern:
        #
        # * LAYOUT_KEY = MODULE + ".auto_layout_website_%d"
        # * ASSETS_KEY = MODULE + ".auto_assets_website_%d"
        # * VIEW_KEY = MODULE + ".auto_view_%d_%d"
        name = view.model_data_id.name
        if 'auto_view_' in name:
            origin_view_id = int(name.split('_')[-1])
        elif 'auto_layout_website_' in name:
            origin_view_id = env.ref("website_multi_theme.layout_pattern").id
        elif 'auto_assets_website_' in name:
            origin_view_id = env.ref("website_multi_theme.assets_pattern").id

        _logger.debug('set origin_view_id %s for view %s',
                      origin_view_id, view.id)
        view.write({'origin_view_id': origin_view_id})

    # remove column
    cr.execute("ALTER TABLE ir_ui_view DROP COLUMN multi_theme_generated_tmp")
