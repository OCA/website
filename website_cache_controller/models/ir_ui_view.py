import lxml

from odoo import api, models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def get_html_from_string(self, res, full_html=None):
        """Get lxml etree object from string (complete or partial)"""
        if full_html:
            html = lxml.html.fromstring(res)
        else:
            html = lxml.html.document_fromstring(res)[0]
        return html

    def get_cache_paths_view(self, res):
        """Return an altered view by replacing public images paths from
        '/web/image/X' to '/website/cache/image/X'"""

        website_id = self.env.context.get("website_id")

        # Cache path destined for frontend and public/portal users only
        if not website_id:
            return res

        full_html = lxml.html._looks_like_full_html_bytes(res)

        try:
            html = self.get_html_from_string(res.decode('UTF-8'), full_html)
        except ValueError:
            html = self.get_html_from_string(res, full_html)
        except Exception:
            return res

        # Replace occurances of /web/image only inside attributes
        elements = html.xpath(
            "//*[attribute::*[contains(., '/web/image/')]]"
        )

        if not elements:
            return res

        for el in elements:
            cache_attrs = {
                k: v.replace('/web/image', '/website/cache/image')
                for k, v in el.attrib.items() if '/web/image' in v
            }
            el.attrib.update(cache_attrs)

        html = lxml.etree.tostring(html, method='html', encoding='UTF-8')

        return html

    @api.multi
    def render(self, values=None, engine='ir.qweb', minimal_qcontext=False):
        res = super(IrUiView, self).render(
            values=values, engine=engine, minimal_qcontext=minimal_qcontext
        )
        res = self.get_cache_paths_view(res)
        return res
