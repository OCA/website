# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, an open source suite of business apps
# This module copyright (C) 2015 bloopark systems (<http://bloopark.de>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import api, fields, models
from openerp.addons.website_seo.models.website import slug
from openerp.http import request


class View(models.Model):

    """Update view model with additional SEO variables."""

    _name = 'ir.ui.view'
    _inherit = ['ir.ui.view', 'website.seo.metadata']

    # ToDo: if the automatically setup of the field seo_url_level is done when
    # the seo_url_parent is changed set readonly to True
    # ToDo: check and move if needed the two fields to website.seo.metadata,
    # I think it will be necessary when the website_seo_blog module is updated
    # with the same seo url handling like in the website_seo module
    seo_url_level = fields.Integer(
        string='SEO Url Level', readonly=False,
        help='Indicates the SEO url level. It starts with the root level 0.')
    seo_url_parent = fields.Many2one(
        'ir.ui.view', string='SEO Parent',
        domain=[('type', '=', 'qweb'), ('inherit_id', '=', False)],
        help='The SEO Parent field is used to describe hierarchical urls like '
        '"/ecommerce/study/how-to-do-it-right". Taking this as example you '
        'have to create 3 pages (ir.ui.view records) for "ecommerce", "study" '
        'and "how-to-do-it-right". The "ecommerce" page is the first level '
        'part and it doesn\'t need a SEO parent. The "study" page is the '
        'second level part and it needs the parent page "ecommerce". The '
        '"how-to-do-it-right" page is the third part and it needs the parent '
        'page "study". If all pages are configured correct the page '
        '"how-to-do-it-right" is rendered when calling '
        '"/ecommerce/study/how-to-do-it-right".'
    )

    @api.multi
    def writeToDo(self, vals):
        # ToDo: add automatically setup of the field seo_url_level when the
        # seo_url_parent is changed, maybe use an onchange event instead of the
        # write() function
        # old_seo_url_parent = False
        # check_views = False
        if 'seo_url_parent' in vals:
            # check_views = True
            if vals['seo_url_parent']:
                parent = self.browse(vals['seo_url_parent'])
                vals['seo_url_level'] = parent.seo_url_level + 1
                # old_seo_url_parent = parent
            else:
                # if self.seo_url_parent:
                    # old_seo_url_parent = self.seo_url_parent
                vals['seo_url_level'] = 0

        res = super(View, self).write(vals)

        # ToDo: update all related views with the correct seo_url_level and
        # seo_url_parent
        # if old_seo_url_parent:

        return res

    @api.cr_uid_ids_context
    def render(self, cr, uid, id_or_xml_id, values=None, engine='ir.qweb',
               context=None):
        """Add additional helper variables.

        Add slug function with additional seo url handling and the query string
        of the http request environment to the values object.
        """
        if values is None:
            values = {}

        values.update({
            'slug': slug,
            'request_query_string': request.httprequest.environ['QUERY_STRING']
        })

        return super(View, self).render(cr, uid, id_or_xml_id, values=values,
                                        engine=engine, context=context)
