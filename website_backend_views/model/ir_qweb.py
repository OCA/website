# -*- coding: utf-8 -*-
# Copyright 2015 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

try:
    import json as json
except ImportError:
    import json
from lxml import etree
from openerp import models, _


class IrQweb(models.Model):
    _inherit = 'ir.qweb'

    def render_tag_website_backend_view(
            self, element, template_attributes, generated_attributes,
            qwebcontext):
        options = json.loads(
            template_attributes.get('website-backend-view', '{}'))
        model = self.pool.get(options.get('res_model'))
        if not model:
            raise NameError(
                _('Unknown model "%s" or no model defined') %
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
                'data-website-backend-view-domain': json.dumps(
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
