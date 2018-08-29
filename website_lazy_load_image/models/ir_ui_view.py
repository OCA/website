# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from lxml import etree


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    LAZYLOAD_DEFAULT_SRC = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///' \
                           'wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='

    @api.model
    def render_template(self, template, values=None, engine='ir.qweb'):
        """Replaces the src attribute with a data-src attribute
        for all img elements without the 'lazyload-disable' css class.
        We use LAZYLOAD_DEFAULT_SRC to prevent showing a broken image
        icon when the JS is not loading yet.
        """
        res = super(IrUiView, self).render_template(template, values, engine)
        website_id = self.env.context.get('website_id')
        if website_id and not \
                self.env['website'].browse(website_id).is_publisher():
            html = etree.HTML(res)
            imgs = html.xpath(
                '//main//img[@src][not(hasclass("lazyload-disable"))]'
            ) + html.xpath(
                '//footer//img[@src][not(hasclass("lazyload-disable"))]'
            )
            for img in imgs:
                src = img.attrib['src']
                img.attrib['src'] = self.LAZYLOAD_DEFAULT_SRC
                img.attrib['data-src'] = src
            res = etree.tostring(html, method='html')
        return res
