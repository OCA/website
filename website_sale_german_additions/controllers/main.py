from openerp import http
from openerp.http import request

class website_sale_german_additions(http.Controller):
    @http.route(['/page/terms', '/page/website.terms'], type='http', auth='public', website=True)
    def wsga_terms(self, **kw):
        return http.request.render('website_sale_german_additions.wsga_terms')
        
    @http.route(['/page/revocation', '/page/website.revocation'], type='http', auth='public', website=True)
    def wsga_revocation(self, **kw):
        return http.request.render('website_sale_german_additions.wsga_revocation')
        
    @http.route(['/page/delivery', '/page/website.delivery'], type='http', auth='public', website=True)
    def wsga_delivery(self, **kw):
        return http.request.render('website_sale_german_additions.wsga_delivery')
        
    @http.route(['/page/privacy', '/page/website.privacy'], type='http', auth='public', website=True)
    def wsga_privacy(self, **kw):
        return http.request.render('website_sale_german_additions.wsga_privacy')

    @http.route(['/page/imprint', '/page/website.imprint'], type='http', auth='public', website=True)
    def wsga_privacy(self, **kw):
        return http.request.render('website_sale_german_additions.wsga_imprint')
        
class wsga_popover(http.Controller):
    @http.route('/popover/terms/', auth="public", type='http')
    def wsga_popover_terms(self, **kw):
        imd = request.registry['ir.model.data']
        iuv = request.registry['ir.ui.view']

        view_id = imd.get_object_reference(request.cr, request.uid, 'website_sale_german_additions', 'wsga_terms')
        view = iuv.browse(request.cr, request.uid, [(view_id[1])], context=None)
        
        xml_id = view_id[1]
        view_result = view[0].arch
        
        return http.request.render('website_sale_german_additions.wsga_popover_terms', {'html_view': view_result})
        
    @http.route('/popover/revocation/', auth="public", type='http')
    def wsga_popover_revocation(self, **kw):
        imd = request.registry['ir.model.data']
        iuv = request.registry['ir.ui.view']

        view_id = imd.get_object_reference(request.cr, request.uid, 'website_sale_german_additions', 'wsga_revocation')
        view = iuv.browse(request.cr, request.uid, [(view_id[1])], context=None)
        
        xml_id = view_id[1]
        view_result = view[0].arch
        
        return http.request.render('website_sale_german_additions.wsga_popover_revocation', {'html_view': view_result})