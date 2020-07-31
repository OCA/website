# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

import lxml

from odoo import api, models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    LAZYLOAD_DEFAULT_SRC = (
        "data:image/gif;base64,R0lGODlhAQABAIAAAP///"
        "wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="
    )

    @api.model
    def render_template(self, template, values=None, engine="ir.qweb"):
        """Replaces the src attribute with a data-src attribute
        for all img elements without the 'lazyload-disable' css class.
        We use LAZYLOAD_DEFAULT_SRC to prevent showing a broken image
        icon when the JS is not loading yet.
        """
        res = super(IrUiView, self).render_template(template, values, engine)
        website_id = self.env.context.get("website_id")
        if website_id and not self.env["website"].browse(website_id).is_publisher():
            html = lxml.html.fromstring(res)
            doctype = html.getroottree().docinfo.doctype
            has_doctype = doctype in res.decode("UTF-8")
            if not has_doctype:
                return res
            imgs = html.xpath(
                '//main//img[@src][not(hasclass("lazyload-disable"))]'
            ) + html.xpath('//footer//img[@src][not(hasclass("lazyload-disable"))]')
            for img in imgs:
                src = img.attrib["src"]
                img.attrib["src"] = self.LAZYLOAD_DEFAULT_SRC
                img.attrib["data-src"] = src
            bgs = html.xpath(
                '//main//*[contains(@style, "background-image")]'
                '[not(hasclass("lazyload-disable"))]'
            )
            for bg in bgs:
                style_attr = bg.attrib["style"]
                split_style_attr = style_attr.split(";")
                for rule in split_style_attr:
                    rule_key_value = rule.split(":", 1)
                    if (
                        rule_key_value
                        and len(rule_key_value) == 2
                        and rule_key_value[0] == "background-image"
                        and "url" in rule_key_value[1]
                    ):
                        background_image_url = re.findall(
                            r"url\((?:\'|\")(.*)(?:\'|\"\))", rule_key_value[1]
                        )
                        if background_image_url:
                            bg.attrib["data-src"] = background_image_url[0]
                            bg.attrib["style"] = bg.attrib["style"].replace(rule, "")
                            bg.attrib["class"] += " lazyload-bg"
            res = lxml.etree.tostring(
                html, method="html", encoding="UTF-8", doctype=doctype,
            )
        return res
