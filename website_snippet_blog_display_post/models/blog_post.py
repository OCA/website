# -*- coding: utf-8 -*-
# (C) 2015 Therp BV <http://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html). 

from openerp import models


class BlogPost(models.Model):
    _inherit = 'blog.post'

    def get_post(self, parameter_id, blog_id):
        domain = [('blog_id', '=', blog_id)]
        if parameter_id < 0:
            return self.search(
                domain, order='create_date desc',
                limit=1, offset=-1-parameter_id)
        else:
            return self.browse([parameter_id])
        return self.browse([])
