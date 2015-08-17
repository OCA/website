# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, an open source suite of business apps
# This module copyright (C) 2015 bloopark systems (<http://bloopark.de>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from lxml import etree
from openerp.addons.base.ir import ir_qweb
from openerp.addons.base.ir.ir_qweb import QWebException
from openerp.addons.base.ir.ir_qweb import raise_qweb_exception


class QWeb(ir_qweb.QWeb):

    """QWeb object for rendering stuff in the website context."""

    def render_node(self, element, qwebcontext):
        generated_attributes = ""
        t_render = None
        template_attributes = {}
        for (attribute_name, attribute_value) in element.attrib.iteritems():
            attribute_name = str(attribute_name)
            if attribute_name == "groups":
                cr = qwebcontext.get('request') and qwebcontext[
                    'request'].cr or None
                uid = qwebcontext.get('request') and qwebcontext[
                    'request'].uid or None
                can_see = self.user_has_groups(
                    cr, uid, groups=attribute_value) if cr and uid else False
                if not can_see:
                    return ''

            attribute_value = attribute_value.encode("utf8")

            if attribute_name.startswith("t-"):
                for attribute in self._render_att:
                    if attribute_name[2:].startswith(attribute):
                        attrs = self._render_att[attribute](
                            self, element, attribute_name, attribute_value,
                            qwebcontext)
                        for att, val in attrs:
                            if not val:
                                continue
                            if not isinstance(val, str):
                                val = unicode(val).encode('utf-8')
                            generated_attributes += self.render_attribute(
                                element, att, val, qwebcontext)
                        break
                else:
                    if attribute_name[2:] in self._render_tag:
                        t_render = attribute_name[2:]
                    template_attributes[attribute_name[2:]] = attribute_value
            else:
                generated_attributes += self.render_attribute(
                    element, attribute_name, attribute_value, qwebcontext)

        if 'debug' in template_attributes:
            debugger = template_attributes.get('debug', 'pdb')
            __import__(debugger).set_trace()  # pdb, ipdb, pudb, ...
        if t_render:
            result = self._render_tag[t_render](
                self, element, template_attributes, generated_attributes,
                qwebcontext)
        else:
            result = self.render_element(
                element, template_attributes, generated_attributes,
                qwebcontext)

        if element.tail:
            result += self.render_tail(element.tail, element, qwebcontext)

        if isinstance(result, unicode):
            return result.encode('utf-8')
        return result

    def render_element(
            self, element, template_attributes, generated_attributes,
            qwebcontext, inner=None):
        # element: element
        # template_attributes: t-* attributes
        # generated_attributes: generated attributes
        # qwebcontext: values
        # inner: optional innerXml
        if inner:
            g_inner = inner.encode('utf-8') if isinstance(inner, unicode) \
                else inner
        else:
            g_inner = [] if element.text is None else [self.render_text(
                element.text, element, qwebcontext)]
            for current_node in element.iterchildren(tag=etree.Element):
                try:
                    g_inner.append(self.render_node(current_node, qwebcontext))
                except QWebException:
                    raise
                except Exception:
                    template = qwebcontext.get('__template__')
                    raise_qweb_exception(
                        message="Could not render element %r" % element.tag,
                        node=element, template=template)
        name = str(element.tag)
        inner = "".join(g_inner)
        trim = template_attributes.get("trim", 0)
        if trim == 0:
            pass
        elif trim == 'left':
            inner = inner.lstrip()
        elif trim == 'right':
            inner = inner.rstrip()
        elif trim == 'both':
            inner = inner.strip()
        if name == "t":
            return inner
        elif len(inner) or name not in self._void_elements:
            return "<%s%s>%s</%s>" % tuple(
                qwebcontext if isinstance(qwebcontext, str) else
                qwebcontext.encode('utf-8')
                for qwebcontext in (name, generated_attributes, inner, name)
            )
        else:
            return "<%s%s/>" % (name, generated_attributes)

    def render_text(self, text, element, qwebcontext):
        return text.encode('utf-8')
