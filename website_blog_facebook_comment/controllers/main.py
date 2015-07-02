# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
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

from openerp.addons.web import http
from openerp.addons.website_blog.controllers.main import WebsiteBlog
from openerp.http import request
from openerp.addons.website.models.website import slug


class WebsiteBlog(WebsiteBlog):

    def _base_url(self):
        config_pool = request.registry['ir.config_parameter']
        base_url = config_pool.get_param(
            request.cr, request.uid,
            'web.base.url', default=False)
        if base_url is False or len(base_url) <= 0:
            return False
        return base_url

    @http.route([
        """/blog/<model('blog.blog'):blog>/post/"""
        """<model('blog.post', '[("blog_id","=", "blog[0]")]'):blog_post>"""],
        type='http', auth="public", website=True)
    def blog_post(self, blog, blog_post,
                  tag_id=None, page=1, enable_editor=None, **post):
        response = super(WebsiteBlog, self).blog_post(
            blog, blog_post, tag_id=None, page=1, enable_editor=None, **post)
        response.qcontext['appId'] = request.website.facebook_appid
        response.qcontext['lang'] = request.context['lang']
        response.qcontext['numposts'] = request.website.facebook_numposts
        base_url = (self._base_url() + '/blog/' +
                    str(slug(response.qcontext['blog'])) + '/post/' +
                    str(slug(response.qcontext['blog_post'])))
        response.qcontext['base_url'] = base_url
        return response
