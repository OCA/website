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
import re
from openerp.osv import orm
from openerp.addons.web.http import request


class QWeb(orm.AbstractModel):

    """QWeb object for rendering stuff in the website context."""

    _inherit = 'website.qweb'

    URL_ATTRS = {
        'form': 'action',
        'a': 'href',
    }
    re_remove_spaces = re.compile(r'\s+')
    PRESERVE_WHITESPACE = [
        'pre',
        'textarea',
        'script',
        'style',
    ]

    def render_text(self, text, element, qwebcontext):
        compress = request and not request.debug and request.website and \
            request.website.compress_html
        if compress and element.tag not in self.PRESERVE_WHITESPACE:
            text = self.re_remove_spaces.sub(' ', text.lstrip())
        return super(QWeb, self).render_text(text, element, qwebcontext)

    def render_tail(self, tail, element, qwebcontext):
        compress = request and not request.debug and request.website and \
            request.website.compress_html
        if compress and element.getparent().tag not in \
                self.PRESERVE_WHITESPACE:
            # No need to recurse because those tags children are not html5
            # parser friendly
            tail = self.re_remove_spaces.sub(' ', tail.rstrip())
        return super(QWeb, self).render_tail(tail, element, qwebcontext)
