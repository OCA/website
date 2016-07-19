# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import http
from openerp.addons.website_blog.controllers.main import WebsiteBlog
from openerp.addons.website_blog.controllers.main import QueryURL
from openerp.addons.web.http import request

class WebsiteBlog(WebsiteBlog):

    # note route must allways be the most external

    @http.route([
            '/blog/<model("blog.blog"):blog>/cat/<model("blog.category"):cat>',
            '/blog/<model("blog.blog"):blog>/cat/<model("blog.category"):cat>/page/<int:page>',
            '/cat/<model("blog.category"):cat>',
            '/cat/<model("blog.category"):cat>/page/<int:page>',
        ], type='http', auth="public", website=True)    
    def blogcat(self, blog=None, cat=None, page=1, **opt):
        result = super(WebsiteBlog, self).blog(blog=blog, tag=None, page=1, opt=opt)
        cr, uid, context = request.cr, request.uid, request.context
        blog_cat_object = request.registry['blog.category']
        # categories are not per-blog
        allcat_ids = blog_cat_object.search(cr, uid, [], context=context) 
        domain = [] 
        # comment out for now categories span thoughout all blogs. a semantic choice.
        if blog:
            domain += [('blog_id', '=', blog.id)]
        if cat:
            date_begin, date_end = opt.get('date_begin'), opt.get('date_end')
            if date_begin and date_end:
                domain += [("create_date", ">=", date_begin), ("create_date", "<=", date_end)]
            blog_url = QueryURL(
                    '', ['blog', 'cat', 'tag'], blog=None, tag=None, 
                    cat=cat, date_begin=date_begin, date_end=date_end
                )
            domain += [('category_id', '=', cat.id)]
            blog_post_obj = request.registry['blog.post']
            blog_post_ids = blog_post_obj.search(cr, uid, domain, order="create_date desc", context=context)
            blog_posts = blog_post_obj.browse(cr, uid, blog_post_ids, context=context)
            pager = request.website.pager(
                url=blog_url(),
                total=len(blog_posts),
                page=page,
                step=self._blog_post_per_page,
            )
            pager_begin = (page - 1) * self._blog_post_per_page
            pager_end = page * self._blog_post_per_page
            blog_posts = blog_posts[pager_begin:pager_end]
            result.qcontext['blog'] = blog
            result.qcontext['blog_posts'] = blog_posts
            result.qcontext['pager'] = pager
            result.qcontext['current_category'] = cat
        result.qcontext['categories'] = blog_cat_object.browse(
            cr, uid, allcat_ids, context=context)
        return result
            

        
    @http.route()
    def blog(self, blog=None, tag=None, page=1, **opt):
        result = super(WebsiteBlog, self).blog(
                blog=blog, tag=tag, page=1, opt=opt) 
        blog_cat_object = request.registry['blog.category']
        # categories are not per-blog
        cr, uid, context = request.cr, request.uid, request.context
        allcat_ids = blog_cat_object.search(cr, uid, [], context=context) 
        result.qcontext['categories'] = blog_cat_object.browse(
            cr, uid, allcat_ids, context=context)
        result.qcontext['current_category'] = False
        return result




