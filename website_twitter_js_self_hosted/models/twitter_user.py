# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class twitteruser(models.Model):
    _name = 'twitter.user'

    feed_id = fields.Many2one(
            string='Twitter feed',
            comodel_name='twitter.feed',
        )
    twitter_user_id = fields.Char(string='User Id on twitter')
    twitter_user_screen_name = fields.Char('Screen name')
    twitter_user_name = fields.Char('name')
    mentions = fields.Integer('Number of Mentions')
