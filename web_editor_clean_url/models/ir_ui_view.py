# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from lxml import html

from odoo import models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def save(self, value, xpath=None):
        arch = html.fromstring(value, parser=html.HTMLParser(encoding="utf-8"))
        value = html.tostring(self._web_editor_clean_url_clean_arch(arch))
        return super().save(value, xpath)

    def _web_editor_clean_url_clean_arch(self, arch, configurations=None):
        """
        Clean all urls in given arch
        """
        for xpath, attributes in self._web_editor_clean_url_selectors():
            for element in arch.xpath(xpath):
                self._web_editor_clean_url_clean_element(
                    element, attributes, configurations=configurations
                )
        return arch

    def _web_editor_clean_url_selectors(self):
        """
        Return xpaths for to find elements with urls to be cleaned and the attributes
        containing them
        """
        return [
            ("//a[@href]", ("href",)),
        ]

    def _web_editor_clean_url_clean_element(
        self, element, attributes, configurations=None
    ):
        """
        Clean urls of element found in attributes
        """
        for attribute in attributes:
            if not element.get(attribute):
                continue
            element.attrib[attribute] = self._web_editor_clean_url(
                element.attrib[attribute],
                configurations=configurations,
            )

    def _web_editor_clean_url(self, url, configurations=None):
        """
        Clean url
        """
        for configuration in configurations or self.env[
            "web.editor.clean.url.configuration"
        ].sudo().search([]):
            url = configuration.clean_url(url)
        return url
