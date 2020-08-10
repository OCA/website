# Copyright 2020 Radovan Skolnik <radovan@skolnik.info>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Menu(models.Model):

    _inherit = "website.menu"

    icon = fields.Char("Icon", required=False, translate=True)
    icon_type = fields.Selection(
        [("image", "Image"), ("icon", "Icon")],
        string="Type",
        required=False,
        translate=False,
    )

    @api.model
    def get_tree(self, website_id, menu_id=None):
        def append_tree(menu_node):
            node = self.browse(menu_node["fields"]["id"])
            menu_node["fields"]["icon_type"] = node.icon_type
            menu_node["fields"]["icon"] = node.icon
            for child in menu_node["children"]:
                append_tree(child)
            return menu_node

        return append_tree(super().get_tree(website_id, menu_id))
