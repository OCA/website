# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import simplejson
from lxml import etree
from openerp import models


class WebsiteQweb(models.Model):
    _inherit = 'website.qweb'

    def render_tag_website_backend_view(
            self, element, template_attributes, generated_attributes,
            qwebcontext):
        options = simplejson.loads(
            template_attributes.get('website-backend-view', '{}'))
        model = self.pool.get(options.get('res_model'))
        if not model:
            raise NameError(
                'Unknown model "%s" or no model defined' %
                options.get('res_model'))
        # we do the nested divs only in for the backend's css rules to work
        etree.SubElement(
            etree.SubElement(
                etree.SubElement(
                    element,
                    'div',
                    attrib={
                        'class': 'openerp',
                    }),
                'div',
                attrib={
                    'class': 'oe_application oe_webclient',
                }),
            'div',
            attrib={
                'data-website-backend-view-model': model._name,
                'data-website-backend-view-type': options.get(
                    'view_type', 'form'),
                'data-website-backend-view-id': options.get('view_id', ''),
                'data-website-backend-view-res-id': str(
                    options.get('res_id', '')),
                'data-website-backend-view-domain': simplejson.dumps(
                    options.get('domain', '{}')),
            })
        etree.SubElement(
            element,
            't',
            attrib={
                't-set': 'website_backend_views_active',
                't-value': 'True',
            })
        return self.render_element(
            element, template_attributes, generated_attributes,
            qwebcontext)
