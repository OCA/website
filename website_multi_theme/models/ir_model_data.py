# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging

from odoo import models, api


_logger = logging.getLogger(__name__)


class IrModelData(models.Model):
    _inherit = 'ir.model.data'

    @api.model
    def create(self, vals):
        """Catch cases of creating customize_show views. Reload theme to make new
        customize_show view available right after new module installation. It's
        also needed for CI tests when another modules expects new item in
        "Customize menu".

        We cannot override ir.ui.view model to do it, because it's created
        before creating ir.model.data, which is essential for
        multi_theme_reload

        FIXME: themes are reloaded as much times as new module has views with
        customize_show
        """

        res = super(IrModelData, self).create(vals)
        if (vals.get('model') == 'ir.ui.view' and
                not self.env.context.get('duplicate_view_for_website')):
            view = self.env['ir.ui.view'].browse(vals.get('res_id'))
            if view.customize_show:
                _logger.debug('Call multi_theme_reload '
                              'after creating Customize View "%s"',
                              vals.get('name'))
                self.env['res.config.settings'].multi_theme_reload()
        return res
