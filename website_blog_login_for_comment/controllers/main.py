# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
#                 Antonio Espinosa <antonioea@antiun.com>
#                 Javier Iniesta <javieria@antiun.com>
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

import urllib
import werkzeug

from openerp import SUPERUSER_ID
from openerp.addons.web.http import request
from openerp.addons.web import http
from openerp.addons.website.models.website import slug
from openerp.tools.translate import _
from openerp.addons.website_blog.controllers.main import WebsiteBlog


class WebsiteBlog(WebsiteBlog):

    def _blog_post_message(self, blog_post_id, message_content, **post):
        cr, uid, context = request.cr, request.uid, request.context
        BlogPost = request.registry['blog.post']
        User = request.registry['res.users']
        # for now, only portal and user can post comment on blog post.
        if uid == request.website.user_id.id:
            raise Warning(_('Public user cannot post comments on blog post.'))
        # get the partner of the current user
        user = User.browse(cr, uid, uid, context=context)
        partner_id = user.partner_id.id

        message_id = BlogPost.message_post(
            cr, SUPERUSER_ID, int(blog_post_id),
            body=message_content,
            type='comment',
            subtype='mt_comment',
            author_id=partner_id,
            path=post.get('path', False),
            context=context)
        return message_id

    @http.route(['/blogpost/comment'], type='http', auth="public",
                methods=['GET', 'POST'], website=True)
    def blog_post_comment(self, blog_post_id=0, **kw):
        cr, uid, context = request.cr, request.uid, request.context
        redirect_url = request.httprequest.referrer + "#comments"
        if kw.get('comment'):
            if not request.session.uid:  # if not logged, redirect to the login
                                         # form, keeping the url to post the
                                         # comment
                kw['comment'] = kw.get('comment').encode('utf8')  # avoid crash
                                                                  # from
                                                                  # urlencode
                                                                  # if accent
                url = '/blogpost/comment/?blog_post_id=%s&%s' % (
                    blog_post_id, urllib.urlencode(kw))
                redirect_url = '/web/login?redirect=%s' % urllib.quote(url)
            else:
                blog_post_id = int(blog_post_id)
                blog_post = request.registry['blog.post']
                post = blog_post.browse(cr, uid, blog_post_id, context=context)
                self._blog_post_message(blog_post_id, kw.get('comment'), **kw)
                redirect_url = "/blog/%s/post/%s#comments" % (
                    slug(post.blog_id), slug(post))
        return werkzeug.utils.redirect(redirect_url)
