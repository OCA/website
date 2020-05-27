# Copyright 2020 Odoo
# Copyright 2020 Tecnativa - Alexandre Díaz
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models
from odoo.tools.translate import html_translate


class Menu(models.Model):
    _inherit = "website.menu"

    def _compute_field_is_mega_menu(self):
        for menu in self:
            menu.is_mega_menu = bool(menu.mega_menu_content)

    def _set_field_is_mega_menu(self):
        for menu in self:
            if menu.is_mega_menu:
                if not menu.mega_menu_content:
                    default_content = self.env["ir.ui.view"].render_template(
                        "website_megamenu.s_mega_menu_multi_menus"
                    )
                    menu.mega_menu_content = default_content.decode()
            else:
                menu.mega_menu_content = False
                menu.mega_menu_classes = False

    is_mega_menu = fields.Boolean(
        compute=_compute_field_is_mega_menu, inverse=_set_field_is_mega_menu
    )
    mega_menu_content = fields.Html(
        translate=html_translate, sanitize=False, prefetch=True
    )
    mega_menu_classes = fields.Char()

    @api.model
    def get_tree(self, website_id, menu_id=None):
        res = super().get_tree(website_id, menu_id=menu_id)
        if menu_id:
            menu = self.browse(menu_id)
        else:
            menu = self.env["website"].browse(website_id).menu_id
        res["is_mega_menu"] = menu.is_mega_menu
        return res
