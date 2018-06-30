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
import collections
from openerp.osv import orm
from openerp.addons.web.http import request


class QWeb(orm.AbstractModel):

    """
    QWeb object for rendering stuff in the website context.
    """
    _inherit = 'website.qweb'

    CDN_TRIGGERS = {
        'link':    'href',
        'script':  'src',
        'img':     'src',
    }

    def render_attribute(self, element, name, value, qwebcontext):
        context = qwebcontext.context or {}
        if not context.get('rendering_bundle'):
            if name == self.URL_ATTRS.get(element.tag):
                value = qwebcontext.get('url_for')(value)
            if request and request.website and request.website.cdn_activated\
                    and name == self.CDN_TRIGGERS.get(element.tag):
                value = request.website.get_cdn_url(value)

        return super(QWeb, self).render_attribute(
            element, name, value, qwebcontext)

    def render_tag_call_assets(
            self, element, template_attributes, generated_attributes,
            qwebcontext):
        if request and request.website and request.website.cdn_activated:
            if qwebcontext.context is None:
                qwebcontext.context = {}
            qwebcontext.context['url_for'] = request.website.get_cdn_url
        return super(QWeb, self).render_tag_call_assets(
            element, template_attributes, generated_attributes, qwebcontext)

    def render_att_att(
            self, element, attribute_name, attribute_value, qwebcontext):
        if attribute_name.startswith("t-attf-"):
            return [(attribute_name[7:], self.eval_format(
                attribute_value, qwebcontext))]

        if attribute_name.startswith("t-att-"):
            return [(attribute_name[6:], self.eval(
                attribute_value, qwebcontext))]

        result = self.eval_object(attribute_value, qwebcontext)
        if isinstance(result, collections.Mapping):
            return result.iteritems()
        # assume tuple
        return [result]
