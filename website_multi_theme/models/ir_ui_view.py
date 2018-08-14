# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging
from lxml import etree

from odoo import fields, models, api
from odoo.http import request


_logger = logging.getLogger(__name__)


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    was_active = fields.Boolean(
        readonly=True,
        help="Indicates if the view was originally active before converting "
             "the single website theme that owns it to multi website mode.",
    )
    origin_view_id = fields.Many2one(
        "ir.ui.view",
        string="Copied from",
        readonly=True,
        help="View from where this one was copied for multi-website"
    )
    multitheme_copy_ids = fields.One2many(
        "ir.ui.view",
        "origin_view_id",
        string="Copies",
        readonly=True,
        help="Duplicates of this view"
    )

    @api.model
    def get_related_views(self, key, bundles=False):
        """This method is used to prepare items
           in 'Customize' menu of website Editor"""
        views = super(IrUiView, self).get_related_views(
            key, bundles=bundles
        )
        current_website = request.website
        current_website_only = self.env.context.get('current_website_only')
        return views.filtered(
            lambda v:
            not v.website_id and not current_website_only
            or v.website_id == current_website
        )

    @api.multi
    def _replace_parent(self, new_parent):
        for view in self:
            view.inherit_id = new_parent
            data = etree.fromstring(view.arch)
            data.attrib["inherit_id"] = new_parent.key
            view.arch = etree.tostring(data)

    # Workaround for https://github.com/odoo/odoo/pull/24429
    def search(self, domain, offset=0, limit=None, order=None, count=False):
        if self.env.context.get('search_multi_website_snippet'):
            website_id = self.env.context['search_multi_website_snippet']
            domain += [
                '|',
                ('website_id', '=', website_id),
                ('website_id', '=', False)
            ]
            order = 'website_id DESC'
            limit = 1
            _logger.debug('Updated domain: %s', domain)

        res = super(IrUiView, self).search(
            domain, offset=offset, limit=limit, order=order, count=count)

        return res
