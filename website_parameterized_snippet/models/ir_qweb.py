# -*- coding: utf-8 -*-
# (C) 2015 Therp BV <http://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models
from lxml import html
from lxml import etree


class HTML(models.AbstractModel):
    _inherit = 'website.qweb.field.html'

    def to_html(self, cr, uid, field_name, record, options,
                source_element, t_att, g_att, qweb_context, context=None):
        document = super(HTML, self).to_html(
            cr, uid, field_name, record, options,
            source_element, t_att, g_att, qweb_context, context=context)
        # render t-call element inserted by dynamic snippets
        parser = etree.HTMLParser(encoding='utf-8')
        dom = html.fromstring(document, parser=parser)
        qweb = self.pool['ir.qweb']
        for t_call in dom.xpath('//t[@t-call]'):
            t_att = t_att.copy()
            t_att['call'] = t_call.get('t-call')
            val = qweb.render_tag_call(
                t_call, t_att, g_att, qweb_context)
            try:
                el = html.fromstring(val, parser=parser)
                parent = t_call.getparent()
                parent.append(el)
                parent.replace(t_call, el)
            except:
                pass
        return html.tostring(dom, encoding='utf-8')
