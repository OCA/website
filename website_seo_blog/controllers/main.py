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
from openerp import SUPERUSER_ID
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.addons.website_blog.controllers.main import QueryURL, WebsiteBlog
from openerp.addons.website_seo.models.website import slug
from openerp.osv.orm import browse_record

import werkzeug


class QueryURL(QueryURL):

    """Copy of QueryURL class of website_blog module to handle SEO urls."""

    def __call__(self, path=None, path_args=None, **kw):
        """Update the url generation to use the new SEO url structure."""
        path = path or self.path
        for k, v in self.args.items():
            kw.setdefault(k, v)
        path_args = set(path_args or []).union(self.path_args)
        paths, fragments = [], []
        for key, value in kw.items():
            if value and key in path_args:
                if isinstance(value, browse_record):
                    paths.append((key, slug(value)))
                else:
                    paths.append((key, value))
            elif value:
                if isinstance(value, list) or isinstance(value, set):
                    fragments.append(
                        werkzeug.url_encode([(key, item) for item in value]))
                else:
                    fragments.append(werkzeug.url_encode([(key, value)]))
        for key, value in paths:
            if key == 'blog':
                # SEO url for blog
                path += '/blog-%s' % value
            elif key == 'post':
                # SEO url for blog post
                path += '/%s' % value
            else:
                path += '/' + key + '/%s' % value
        if fragments:
            path += '?' + '&'.join(fragments)
        return path


class WebsiteBlog(WebsiteBlog):

    """Add new blog and blog post routes to handle blog SEO urls."""

    @http.route([
        '/blog-<string:seo_url>',
        '/blog-<string:seo_url>/page/<int:page>',
        '/blog-<string:seo_url>/tag/<model("blog.tag"):tag>',
        '/blog-<string:seo_url>/tag/<model("blog.tag"):tag>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def seo_blog(self, seo_url, tag=None, page=1, **opt):
        """Route for blogs with SEO urls."""
        # - request.env.context contains always "'lang': u'en_US'" regardless
        # of the used frontend language which results in not found non english
        # blogs, so we update request.env.context with request.context
        env = request.env(context=request.context)
        if seo_url:
            blogs = env['blog.blog'].search([('seo_url', '=', seo_url)])
            if blogs:
                return self.blog(blogs[0], tag=tag, page=page, **opt)

        return request.redirect('/')

    @http.route(['/blog-<string:seo_url_blog>/<string:seo_url_post>'],
                type='http', auth="public", website=True)
    def seo_blog_post(self, seo_url_blog, seo_url_post, tag_id=None, page=1,
                      enable_editor=None, **post):
        """Route for blog posts with SEO urls."""
        # - request.env.user is not set but we need a user for the access of
        # the field website_message_ids in the controller function blog_post()
        # in addons/website_blog/controllers/main.py, if request.env.user is
        # not set you will get an InternalError because of a non set partner_id
        # later
        # - furthermore request.env.context contains always "'lang': u'en_US'"
        # regardless of the used frontend language which results in not found
        # non english blog posts, so we update request.env.context with
        # request.context
        env = request.env(user=SUPERUSER_ID, context=request.context)
        if seo_url_blog and seo_url_post:
            blogs = env['blog.blog'].search([('seo_url', '=', seo_url_blog)])
            if blogs:
                blog_posts = env['blog.post'].search([
                    ('blog_id', '=', blogs[0].id),
                    ('seo_url', '=', seo_url_post)
                ])
                if blog_posts:
                    return self.blog_post(
                        blogs[0], blog_posts[0], tag_id=tag_id, page=1,
                        enable_editor=enable_editor, **post)
                else:
                    return request.redirect("/blog-%s" % (slug(blogs[0])))

        return request.redirect('/')

    @http.route()
    def blogs(self, page=1, **post):
        """Update blog url of original blogs function with SEO url."""
        response = super(WebsiteBlog, self).blogs(page=page, **post)
        response.qcontext.update({'blog_url': QueryURL('', ['blog', 'tag'])})

        return request.website.render(response.template, response.qcontext)

    @http.route()
    def blog(self, blog=None, tag=None, page=1, **opt):
        """Update blog url and pager of original blog function with SEO url."""
        # - request.env.context contains always "'lang': u'en_US'" regardless
        # of the used frontend language which results in not found non english
        # blogs, so we update request.env.context with request.context
        env = request.env(context=request.context)
        blog_post_obj = env['blog.post']
        date_end = opt.get('date_end')
        response = super(WebsiteBlog, self).blog(blog=blog, tag=tag, page=page,
                                                 **opt)
        values = response.qcontext
        blog_url = QueryURL('', ['blog', 'tag'], blog=blog, tag=tag,
                            date_begin=values['date'], date_end=date_end)

        domain = []
        if blog:
            domain += [('blog_id', '=', blog.id)]
        if tag:
            domain += [('tag_ids', 'in', tag.id)]
        if values['date'] and date_end:
            domain += [("create_date", ">=", values['date']),
                       ("create_date", "<=", date_end)]

        blog_posts = blog_post_obj.search(domain, order="create_date desc")

        pager = request.website.pager(
            url=blog_url(),
            total=len(blog_posts),
            page=page,
            step=self._blog_post_per_page,
        )

        values.update({
            'blog_url': blog_url,
            'pager': pager
        })

        return request.website.render(response.template, values)

    @http.route()
    def blog_post(self, blog, blog_post, tag_id=None, page=1,
                  enable_editor=None, **post):
        """Update blog url of original blog_post function with SEO url."""
        date_end = post.get('date_end')
        response = super(WebsiteBlog, self).blog_post(
            blog=blog, blog_post=blog_post, tag_id=tag_id, page=page,
            enable_editor=enable_editor, **post)
        values = response.qcontext
        values.update({'blog_url': QueryURL(
            '', ['blog', 'tag'], blog=blog_post.blog_id, tag=values['tag'],
            date_begin=values['date'], date_end=date_end)})

        return request.website.render(response.template, values)
