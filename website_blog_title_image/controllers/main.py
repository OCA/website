
from openerp.addons.web import http
from openerp.addons.web.http import request

class BlogController(http.Controller):
    
    @http.route('/blogpost/change_title_image', type='json', auth="public", website=True)
    def change_title_image(self, post_id=0, image=None, **post):
        if not post_id:
            return False
        return request.registry['blog.post'].write(request.cr, request.uid, [int(post_id)], {'title_image': image}, request.context)
