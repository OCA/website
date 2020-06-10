import werkzeug
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Binary

content_image_route = Binary.content_image.routing.copy()
content_common_route = Binary.content_common.routing.copy()

image_routes = content_image_route.get('routes', [])
common_routes = content_common_route.get('routes', [])

content_image_route['routes'] = [
    r.replace("/web/image", "/website/cache/image") for r in image_routes
]

content_common_route['routes'] = [
    r.replace("/web/content", "/website/cache/content") for r in common_routes
]


class WebsiteImageBinary(Binary):

    def proxy_redirect(self, proxy_url, url):
        """Return proxy redirect if user is internal"""
        if not request.env.user.has_group('base.group_user'):
            return False
        # Redirect to original url for internal users
        path = request.httprequest.path
        new_url = path.replace(proxy_url, url)
        query_string = request.httprequest.query_string
        if query_string:
            query_string = query_string.decode("utf-8")
            new_url = "%s?%s" % (new_url, query_string)
        return werkzeug.utils.redirect(new_url, code=302)

    @http.route(**content_common_route)
    def website_content_cache(self, *args, **kw):
        """Controller designed for serving public assets only and providing a
        cacheable path for proxy and CDN"""
        redirect = self.proxy_redirect(
            '/website/cache/content', '/web/content'
        )
        if redirect:
            return redirect
        return self.content_common(*args, **kw)

    @http.route(**content_image_route)
    def website_cache_image(self, *args, **kw):
        """Controller designed for serving public images only and providing a
        cacheable path for proxy and CDN"""
        redirect = self.proxy_redirect(
            '/website/cache/image', '/web/image'
        )
        if redirect:
            return redirect
        return self.content_image(*args, **kw)
