# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
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


class WebsiteBlog(WebsiteBlog):

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
        response.qcontext['base_url'] = request.httprequest.url
        return response
