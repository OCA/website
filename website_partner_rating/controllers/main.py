# -*- coding: utf-8 -*-
import werkzeug
import openerp
from openerp import addons
from openerp import SUPERUSER_ID
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.addons.website.models.website import slug, unslug
from openerp.tools.translate import _
import openerp.http as http
from openerp.http import request

#from openerp import http, SUPERUSER_ID
#from openerp.http import request
#from openerp.tools.translate import _
import openerp.addons.website_crm_partner_assign.controllers.main as website_partner_main
#import werkzeug
import werkzeug.urls
import werkzeug.wrappers


class website_partner_rating_comments( website_partner_main.WebsiteCrmPartnerAssign ):
    """ This method is overloaded for to add messaege_rate and short_description
    in product.template"""
    @http.route(['/partners/partner/comment/<int:partner_id>'], type='http', auth="public", methods=['POST'], website=True)
    def partner_rating( self, partner_id, **post ):
        cr, uid, context = request.cr, request.uid, request.context
        if post.get( 'comment' ):
            message_id1 = request.registry['res.partner'].message_post(
                cr, uid, partner_id,
                body=post.get( 'comment' ),
                type='comment',
                subtype='mt_comment',
            context=dict( context ) )  # mail_create_nosubcribe=True
            review = post.get( 'review', 0 )
            short_description = post.get( 'short_description' )
            cr, uid = request.cr, request.uid
            mail_message1 = request.registry['mail.message']
            mail_message1.write( cr, uid, [message_id1], {'message_rate':review, 'short_description':short_description, 'website_message':True, } )

            return werkzeug.utils.redirect( request.httprequest.referrer + "#comments" )



