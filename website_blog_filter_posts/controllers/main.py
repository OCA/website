import werkzeug

from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.addons.website_blog.controllers.main import WebsiteBlog
from openerp.addons.website.models.website import slug, unslug
from openerp.osv.orm import browse_record


class QueryURL(object):
    def __init__(self, path='', path_args=None, **args):
        self.path = path
        self.args = args
        self.path_args = set(path_args or [])

    def __call__(self, path=None, path_args=None, **kw):
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
                    fragments.append(werkzeug.url_encode([(key, item) for item in value]))
                else:
                    fragments.append(werkzeug.url_encode([(key, value)]))
        for key, value in paths:
            path += '/' + key + '/%s' % value
        if fragments:
            path += '?' + '&'.join(fragments)
        return path


class WebsiteBlog(WebsiteBlog):
    _bppp = 10
    _post_comment_per_page = 10
    _filter_by_year = 0

    @http.route([
        '/blog/<model("blog.blog"):blog>',
        '/blog/<model("blog.blog"):blog>/page/<int:page>',
        '/blog/<model("blog.blog"):blog>/tag/<string:tag>',
        '/blog/<model("blog.blog"):blog>/tag/<string:tag>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def blog(self, blog=None, tag=None, page=1, **opt):
        """ Prepare all values to display the blog.

        :return dict values: values for the templates, containing

         - 'blog': current blog
         - 'blogs': all blogs for navigation
         - 'pager': pager of posts
         - 'active_tag_ids' :  list of active tag ids,
         - 'tags_list' : function to built the comma-separated tag list ids (for the url),
         - 'tags': all tags, for navigation
         - 'nav_list': a dict [year][month] for archives navigation
         - 'date': date_begin optional parameter, used in archives navigation
         - 'blog_url': help object to create URLs
        """

        if 'bp_filter_by_bpp' in request.httprequest.cookies:
            self._bppp = int(request.httprequest.cookies.get('bp_filter_by_bpp'))

        date_begin, date_end = opt.get('date_begin'), opt.get('date_end')

        cr, uid, context = request.cr, request.uid, request.context
        blog_post_obj = request.registry['blog.post']

        blog_obj = request.registry['blog.blog']
        blog_ids = blog_obj.search(cr, uid, [], order="create_date asc", context=context)
        blogs = blog_obj.browse(cr, uid, blog_ids, context=context)

        # build the domain for blog post to display
        domain = []
        # retrocompatibility to accept tag as slug
        active_tag_ids = tag and map(int, [unslug(t)[1] for t in tag.split(',')]) or []
        if active_tag_ids:
            domain += [('tag_ids', 'in', active_tag_ids)]
        if blog:
            domain += [('blog_id', '=', blog.id)]
        if date_begin and date_end:
            domain += [("create_date", ">=", date_begin), ("create_date", "<=", date_end)]

        blog_url = QueryURL('', ['blog', 'tag'], blog=blog, tag=tag, date_begin=date_begin, date_end=date_end)

        selected_order = 'create_date desc'
        user_filter = request.httprequest.cookies.get('bp_filter_by_date');
        if user_filter == 'newest':
            selected_order = 'create_date desc'
        elif user_filter == 'oldest':
            selected_order = 'create_date asc'

        #--------------------------------------
        if 'bp_filter_by_year' in request.httprequest.cookies:
            _filter_by_year = request.httprequest.cookies.get('bp_filter_by_year')
            domain += [('create_date', 'ilike', _filter_by_year)]

        blog_post_ids = blog_post_obj.search(cr, uid, domain, order=selected_order, context=context)
        blog_posts = blog_post_obj.browse(cr, uid, blog_post_ids, context=context)

        pager = request.website.pager(
            url=blog_url(),
            total=len(blog_posts),
            page=page,
            step=self._bppp,
        )
        pager_begin = (page - 1) * self._bppp
        pager_end = page * self._bppp
        blog_posts = blog_posts[pager_begin:pager_end]

        all_tags = blog.all_tags()[blog.id]

        # function to create the string list of tag ids, and toggle a given one.
        # used in the 'Tags Cloud' template.
        def tags_list(tag_ids, current_tag):
            tag_ids = list(tag_ids) # required to avoid using the same list
            if current_tag in tag_ids:
                tag_ids.remove(current_tag)
            else:
                tag_ids.append(current_tag)
            tag_ids = request.registry['blog.tag'].browse(cr, uid, tag_ids, context=context).exists()
            return ','.join(map(slug, tag_ids))

        values = {
            'blog': blog,
            'blogs': blogs,
            'tags': all_tags,
            'active_tag_ids': active_tag_ids,
            'tags_list' : tags_list,
            'blog_posts': blog_posts,
            'pager': pager,
            'nav_list': self.nav_list(blog),
            'blog_url': blog_url,
            'date': date_begin,
        }
        response = request.website.render("website_blog.blog_post_short", values)
        return response
