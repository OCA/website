# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    @api.multi
    def get_parents(self, revert=False, include_self=False):
        """List current menu's parents.

        :param bool revert:
            Indicates if the result must be revert before returning.
            Activating this will mean that the result will be ordered from
            parent to child.

        :param bool include_self:
            Indicates if the current menu item must be included in the result.

        :return list:
            Menu items ordered from child to parent, unless ``revert=True``.
        """
        result = list()
        menu = self if include_self else self.parent_id
        while menu:
            result.append(menu)
            menu = menu.parent_id
        return reversed(result) if revert else result
