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
import re

from openerp import api, fields, models
from openerp.addons.website.models.website import slugify
from openerp.exceptions import ValidationError
from openerp.osv import orm
from openerp.tools.translate import _


def slug(value):
    """Add seo url check in slug handling."""
    if isinstance(value, orm.browse_record):
        # if a seo url field exists in a record and it is not empty return it
        if 'seo_url' in value._fields and value.seo_url:
            return value.seo_url

        # [(id, name)] = value.name_get()
        id, name = value.id, value.display_name
    else:
        # assume name_search result tuple
        id, name = value
    slugname = slugify(name or '').strip().strip('-')
    if not slugname:
        return str(id)
    return "%s-%d" % (slugname, id)


class WebsiteMenu(models.Model):

    """Add translation possibility to website menu entries."""

    _inherit = 'website.menu'

    url = fields.Char(translate=True)


class WebsiteSeoMetadata(models.Model):

    """Add additional SEO fields which can be used by other models."""

    _inherit = 'website.seo.metadata'

    seo_url = fields.Char(
        string='SEO Url', translate=True, help='If you fill out this field '
        'manually the allowed characters are a-z, A-Z, 0-9, - and _.')
    website_meta_robots = fields.Selection([
        ('INDEX,FOLLOW', 'INDEX,FOLLOW'),
        ('NOINDEX,FOLLOW', 'NOINDEX,FOLLOW'),
        ('INDEX,NOFOLLOW', 'INDEX,NOFOLLOW'),
        ('NOINDEX,NOFOLLOW', 'NOINDEX,NOFOLLOW')
    ], string='Website meta robots')

    @api.model
    def create(self, vals):
        """Add check for correct SEO urls.

        Exceptional cases will be handled in the additional website SEO
        modules. For example have a look at the website_seo_blog module in the
        create() function in website_seo_blog/models/website_blog.py.
        """
        if vals.get('seo_url', False):
            self.validate_seo_url(vals['seo_url'])

        return super(WebsiteSeoMetadata, self).create(vals)

    @api.multi
    def write(self, vals):
        """Add check for correct SEO urls."""
        if vals.get('seo_url', False):
            self.validate_seo_url(vals['seo_url'])

        return super(WebsiteSeoMetadata, self).write(vals)

    def validate_seo_url(self, seo_url):
        """Validate a manual entered SEO url."""
        if not seo_url or not bool(re.match('^([.a-zA-Z0-9-_]+)$', seo_url)):
            raise ValidationError(_('Only a-z, A-Z, 0-9, - and _ are allowed '
                                    'characters for the SEO url.'))
        return True
