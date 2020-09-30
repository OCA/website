# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json
import datetime
import random
from odoo import http, tools
from odoo.http import request
from openerp.addons.website_blog.controllers import main


class WebsiteBlog(main.WebsiteBlog):

    _date_begin = None
    _date_end = None
    _tag = None
    _cat = None

    def nav_list_grouped(self):
        blog_post_obj = request.env['blog.post']
        beginning_of_year = datetime.date.strftime(
            datetime.date(datetime.date.today().year, 1, 1),
            tools.DEFAULT_SERVER_DATE_FORMAT
        )
        old_groups = blog_post_obj.read_group(
            [['create_date', '<', beginning_of_year]],
            ['name', 'create_date'],
            groupby="create_date:year",
            orderby="create_date:year desc",
        )
        # the standard orderby is just a comma separated list of fields
        # optionally followed by desc or asc.
        # UNDOCUMENTED FEATURE, the time :year, :month, :day work also
        # for orderby.
        new_groups = blog_post_obj.read_group(
            [['create_date', '>=', beginning_of_year]],
            ['name', 'create_date'],
            groupby="create_date",
            orderby="create_date desc",
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
                group['__domain'][2][2], tools.DEFAULT_SERVER_DATETIME_FORMAT
            ).date()
            end_date = datetime.datetime.strptime(
                group['__domain'][3][2], tools.DEFAULT_SERVER_DATETIME_FORMAT
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
        self._date_begin, self._date_end = opt.get(
            'date_begin'), opt.get('date_end')
        if tag and len(tag.split('-')) > 1:
           self._tag = int(tag.split('-')[-1])
        result = super(WebsiteBlog, self).blog(
            blog=blog, tag=tag, page=page, **opt)
        result.qcontext[
            'nav_list_old_grouped'] = self.nav_list_grouped()['old_groups']
        result.qcontext[
            'nav_list_new_grouped'] = self.nav_list_grouped()['new_groups']
        return result

    @http.route()
    def blog_post(
            self, blog, blog_post, tag_id=None, page=1,
            enable_editor=None, **post):
        blog_post_obj = request.env['blog.post']
        domain = []
        tag_computed = False
        if not tag_id and self._tag:
            _tagid = request.env['blog.tag'].search(
                [('id', '=', self._tag)])
            if _tagid:
                domain += [('tag_ids', '=', _tagid.id)]
                tag_computed = True
        if not tag_id and not self._tag:
            referrer = request.httprequest.referrer.split('/')
            if referrer[-2] == 'tag':
                try:
                    _tagid = request.env['blog.tag'].search(
                        [('id', '=', int(referrer[-1].split('-')[-1]))])
                    if _tagid:
                        domain += [('tag_ids', '=', _tagid.id)]
                        tag_computed = True
                except:
                    pass
        if tag_computed:
            tag_id = _tagid.id
            self._tag = _tagid.id
        if self._date_begin and self._date_end:
            domain += [
                ("create_date", ">=", self._date_begin),
                ("create_date", "<=", self._date_end)
            ]
        result = super(WebsiteBlog, self).blog_post(
            blog=blog, blog_post=blog_post, tag_id=tag_id, page=page,
            enable_editor=enable_editor, **post
        )
        if blog:
            domain += [('blog_id', '=', blog.id)]
        if self._cat:
            domain += [('category_id', '=', self._cat.id)]

        # Find next Post
        all_post_ids = blog_post_obj.search(
            domain, order="post_date desc"
        ).ids
        # should always return at least the current post
        # but if the blogpost id is not present in the current domain we
        # fetched we will just get a random one.
        if blog_post.id not in all_post_ids:
            current_blog_post_index = random.sample(
                list(range(len(all_post_ids))), 1
            )[0]
        else:
            current_blog_post_index = all_post_ids.index(blog_post.id)
        next_post_id = all_post_ids[
            0 if current_blog_post_index >= len(
                all_post_ids) - 1 else current_blog_post_index + 1]
        next_post = next_post_id and blog_post_obj.browse(
            next_post_id) or False
        result.qcontext.update({
            'next_post': next_post,
            'next_post_cover_properties': json.loads(
                next_post.cover_properties) if next_post else {}
            
        })
        return result

    @http.route()
    def blogcat(self, blog=None, cat=None, page=1, **opt):
        self._cat = cat
        result = super(WebsiteBlog, self).blogcat(
            blog=blog, cat=cat, page=page, **opt
        )
        return result
