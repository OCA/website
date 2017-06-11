# -*- coding: utf-8 -*-
# © 2014 OpenERP SA
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.addons.website.models.website import slugify
from openerp.addons.web.http import request
from werkzeug.exceptions import NotFound


class Website(models.Model):
    _inherit = "website"

    body_css_class = fields.Char(
        string="Body CSS class", readonly=True, compute="_body_css_class_get")
    theme_id = fields.Many2one(string="Theme", comodel_name='website.theme')

    @api.depends('theme_id')
    def _body_css_class_get(self):
        for website in self:
            self.body_css_class = self.theme_id.css_slug

    @api.model
    def new_page(self, name, template='website.default_page', ispage=True):
        imd = self.env['ir.model.data']
        template_module, template_name = template.split('.')
        # completely arbitrary max_length
        page_name = slugify(name, max_length=50)
        page_xmlid = "%s.%s" % (template_module, page_name)
        try:
            # existing page
            imd.xmlid_lookup(page_xmlid)
        except ValueError:
            # new page
            template_obj = imd.xmlid_to_object(template)
            page = template_obj.copy({
                'website_id': self.env.context.get('website_id'),
                'key': page_xmlid
            })
            page.write({
                'arch': page.arch.replace(template, page_xmlid),
                'name': page_name,
                'page': ispage,
            })
        return page_xmlid

    @api.model
    def get_current_website(self):
        host = request.httprequest.environ.get('HTTP_HOST', '')
        domain_name = host.split(':')[0]
        website_id = self._get_current_website_id(domain_name) or 1
        request.context['website_id'] = website_id
        return self.browse(website_id)

    @api.multi
    def get_template(self, template):
        if not isinstance(template, (int, long)) and '.' not in template:
            template = 'website.%s' % template
        view_id = self.env['ir.ui.view'].get_view_id(template)
        if not view_id:
            raise NotFound
        return self.env['ir.ui.view'].browse(view_id)
