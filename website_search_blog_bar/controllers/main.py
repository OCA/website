# Copyright 2021 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.http import request
from odoo.osv import expression

from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_blog.controllers.main import WebsiteBlog


class WebsiteBlogSearchBar(WebsiteBlog):
    def _get_search_domain(self, search_val, blog=False):
        domain = []
        website = request.website
        if website.blog_search_title:
            domain = expression.OR([domain, [("name", "ilike", search_val)]])
        if website.blog_search_content:
            domain = expression.OR([domain, [("content", "ilike", search_val)]])
        if website.blog_search_manual_teaser:
            domain = expression.OR([domain, [("teaser_manual", "ilike", search_val)]])
        if blog:
            domain = expression.AND([domain, [("blog_id", "=", blog.id)]])
        return domain

    def _prepare_blog_values_search(self, search_val, blogs, blog=False, page=False):

        BlogPost = request.env["blog.post"]
        domain = self._get_search_domain(search_val, blog)

        posts = BlogPost.search(
            domain,
            offset=(page - 1) * self._blog_post_per_page,
            limit=self._blog_post_per_page,
            order="post_date desc",
        )
        post_ids = posts.ids
        first_post = BlogPost
        if not blog:
            first_post = BlogPost.search(
                domain + [("website_published", "=", True)],
                order="post_date desc, id asc",
                limit=1,
            )

        return {
            "first_post": first_post.with_prefetch(post_ids),
            "tags_list": self.tags_list,
            "posts": posts,
            "active_tag_ids": [],
            "domain": domain,
            "blogs": blogs,
            "blog": blog,
            "blog_url": QueryURL("/blog", ["tag"]),
            "search_val": search_val,
        }

    def create_pager(self, search_val, blog, page, opt):
        domain = self._get_search_domain(search_val, blog)
        total = request.env["blog.post"].search_count(domain)
        return request.website.pager(
            url=request.httprequest.path.partition("/page/")[0],
            total=total,
            page=page,
            step=self._blog_post_per_page,
            url_args=opt,
        )

    @http.route(
        [
            """/blog/search_content""",
            """/blog/search_content/page/<int:page>""",
            """/blog/<model("blog.blog", "[('website_id'"""
            """, 'in', (False, current_website_id))]"):blog>/search_content""",
            """/blog/<model("blog.blog"):blog>/search_content/page/<int:page>""",
        ],
        type="http",
        auth="public",
        website=True,
        csrf=False,
    )
    def blog_search(self, blog=None, page=1, **opt):
        blogs = request.env["blog.blog"].search(
            request.website.website_domain(), order="create_date asc, id asc"
        )
        search_val = opt.get("search_val")
        values = self._prepare_blog_values_search(
            search_val=search_val, blogs=blogs, blog=blog, page=page
        )
        values["pager"] = self.create_pager(search_val, blog, page, opt)
        return request.render("website_blog.blog_post_short", values)
