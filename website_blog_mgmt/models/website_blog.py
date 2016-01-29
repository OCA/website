# -*- coding: utf-8 -*-
# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import datetime


class BlogPost(models.Model):
    _inherit = 'blog.post'
    _order = 'website_publication_date DESC, id DESC'

    website_publication_date = fields.Datetime(
        string='Published on', index=True)

    def _process_publication_date(self, vals):
        """Check if a publication date is given and compute the
        'website_published' if the publication_date is < now
        :param dict vals:
            see :meth:`openerp.models.Model.write` for details
        :return: modified dict vals
        """
        if 'website_publication_date' in vals:
            pub_date = vals.get('website_publication_date', False)
            if pub_date:
                pub_date_dt = fields.Datetime.from_string(pub_date)
                vals['website_published'] = pub_date_dt < datetime.now()
            else:
                vals['website_published'] = False
        elif 'website_published' in vals:
            published = vals['website_published']
            if not published:
                vals['website_publication_date'] = False
            else:
                vals['website_publication_date'] = fields.Datetime.now()
        return vals

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        vals = self._process_publication_date(vals)
        return super(BlogPost, self).create(vals)

    @api.multi
    def write(self, vals):
        vals = self._process_publication_date(vals)
        return super(BlogPost, self).write(vals)

    @api.model
    def cron_publish_posts(self):
        recs = self.search(
            [('website_published', '=', False),
             ('website_publication_date', '<=', fields.Datetime.now())])
        if len(recs):
            return recs.write({'website_published': True})
        return True
