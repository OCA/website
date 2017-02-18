# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class BlogPost(models.Model):
    _inherit = ['blog.post', 'base.localizable.mixin']
    _name = 'blog.post'

    @api.multi
    def action_show_in_map(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/blogmap/%s' % self.mapped('blog_id')[:1].id,
        }

    @api.multi
    def _get_location_url(self):
        self.ensure_one()
        return '/blog/%d/post/%d' % (self.blog_id.id, self.id)
