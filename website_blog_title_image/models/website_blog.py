from openerp.osv import osv, fields

class BlogPost(osv.Model):
    _name = "blog.post"
    _inherit = ['blog.post']
    _columns = {
        'title_image': fields.binary('Title Image')
        }