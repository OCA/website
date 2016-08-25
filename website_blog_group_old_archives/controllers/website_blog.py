# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime
from openerp import http, tools
from openerp.http import request
from openerp.addons.website_blog.controllers.main import WebsiteBlog

class website_blog(WebsiteBlog):

    _blog_post_per_page = 20
    _post_comment_per_page = 10

    def nav_list_grouped(self):
        blog_post_obj = request.registry['blog.post']
        beginning_of_year = datetime.date.strftime(
            datetime.date(datetime.date.today().year, 1, 1),
            tools.DEFAULT_SERVER_DATE_FORMAT
        )
        import pudb
        pudb.set_trace()
        old_groups = blog_post_obj.read_group(
            request.cr, request.uid, 
            [['create_date', '<', beginning_of_year]],
            ['name', 'create_date'],
            groupby="create_date:year", 
            orderby="create_date:year desc", 
            context=request.context
        )       
        # the standard orderby is just a comma separated list of fields
        # optionally followed by desc or asc.
        # UNDOCUMENTED FEATURE, the time :year, :month, :day work also 
        # for orderby.
        new_groups = blog_post_obj.read_group(
            request.cr, request.uid,
            [['create_date', '>=', beginning_of_year]],
            ['name', 'create_date'],
            groupby="create_date", 
            orderby="create_date desc", 
            context=request.context
        )
        for group in new_groups:
            begin_date = datetime.datetime.strptime(
                group['__domain'][0][2], tools.DEFAULT_SERVER_DATETIME_FORMAT
            ).date()
            end_date = datetime.datetime.strptime(
                group['__domain'][1][2], tools.DEFAULT_SERVER_DATETIME_FORMAT
            ).date()
            group['date_begin'] = '%s' % datetime.date.strftime(
                begin_date, tools.DEFAULT_SERVER_DATE_FORMAT
            )
            group['date_end'] = '%s' % datetime.date.strftime(
                end_date, tools.DEFAULT_SERVER_DATE_FORMAT
            )
        for group in old_groups:
            begin_date = datetime.datetime.strptime(
                group['__domain'][0][2], tools.DEFAULT_SERVER_DATETIME_FORMAT
            ).date()
            end_date = datetime.datetime.strptime(
                group['__domain'][1][2], tools.DEFAULT_SERVER_DATETIME_FORMAT
            ).date()
            group['date_begin'] = '%s' % datetime.date.strftime(
                begin_date, tools.DEFAULT_SERVER_DATE_FORMAT
            )
            group['date_end'] = '%s' % datetime.date.strftime(
                end_date, tools.DEFAULT_SERVER_DATE_FORMAT
            )
        return {'new_groups': new_groups, 'old_groups': old_groups}

    @http.route()
    def blog(self, blog=None, tag=None, page=1, **opt):
        result = super(website_blog, self).blog(
                blog=blog, tag=tag, page=page, **opt
            )
        import pudb
        pudb.set_trace()
        result.qcontext['nav_list_old_grouped'] = self.nav_list_grouped()['old_groups']
        result.qcontext['nav_list_new_grouped'] = self.nav_list_grouped()['new_groups']
	return result

