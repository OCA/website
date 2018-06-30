# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class WebsiteTweet(models.Model):
    _name = 'twitter.tweet'

    feed_id = fields.Many2one(
        string='Twitter feed',
        comodel_name='twitter.feed',
        required=True,
        ondelete="cascade"
    )
    twitter_user_id = fields.Char(string='User ID on twitter')
    tweet_id = fields.Char(string='original twitter id')
    text = fields.Text(string='Tweet text')
    author = fields.Char(string='Author')
    tweet_create_date = fields.Datetime(string='Date')
