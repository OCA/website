# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class WebsitePublishedMixin(osv.AbstractModel):
    _name = "website.published.mixin"

    _website_url_proxy = lambda self, *a, **kw: self._website_url(*a, **kw)

    _columns = {
        'website_published': fields.boolean('Visible in Website', copy=False),
        'website_url': fields.function(
            _website_url_proxy, type='char', string='Website URL',
            help='The full URL to access the document through the website.'),
    }

    def _website_url(self, cr, uid, ids, field_name, arg, context=None):
        return dict.fromkeys(ids, '#')

    def open_website_url(self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.act_url',
            'url': self.browse(cr, uid, ids[0]).website_url,
            'target': 'self',
        }
