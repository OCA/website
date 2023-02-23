# Copyright 2020 Onestein (<https://www.onestein.nl>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from lxml import etree

from odoo import SUPERUSER_ID, api, fields, models


class WebsiteConfigSettings(models.TransientModel):
    _name = "website.config.settings"
    _inherit = ["res.config.settings"]
    _description = "Website Settings"

    def execute(self):
        if self.user_has_groups("website_security.group_website_security_config"):
            return super(WebsiteConfigSettings, self.sudo()).execute()
        return super(WebsiteConfigSettings, self).execute()

    @api.model
    def _get_website_settings_xpaths(self):
        return ["//div[@data-key='website']"]

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        """Copy and paste the website settings from res.config.settings into this view"""
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type != "form":
            return res
        xml_tree = etree.XML(res["arch"])
        settings_container_element = xml_tree.xpath("//div[hasclass('settings')]")[0]
        settings_res = (
            self.env["res.config.settings"].with_user(SUPERUSER_ID).get_view()
        )
        xml_settings_tree = etree.XML(settings_res["arch"])
        for xpath in self._get_website_settings_xpaths():
            found_elements = xml_settings_tree.xpath(xpath)
            for found_element in found_elements:
                settings_container_element.append(found_element)
        res["arch"] = etree.tostring(xml_tree, encoding="unicode")
        res["models"] = {
            "website.config.settings": settings_res["models"]["res.config.settings"]
        }
        return res
