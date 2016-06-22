# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class BlogPost(models.Model):
    _inherit = 'blog.post'

    title_image = fields.Binary('Title Image')
