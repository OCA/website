# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models
import base64
import json
import re
import urllib
import urllib2


class TwitterFeed(models.Model):
    _name = 'twitter.feed'

    name = fields.Char(
        string='Feed Name',
        help='Just a name to identify this feed',
        required=True
    )
    twitter_api_key = fields.Char(
        string='Twitter API Key',
        help="Twitter API key you can get it from "
        "https://apps.twitter.com/app/new",
        required=True
    )
    twitter_api_secret = fields.Char(
        string='Twitter API secret',
        help="Twitter API secret you can get it from "
        "https://apps.twitter.com/app/new",
        required=True
    )
    twitter_screen_name = fields.Char(
        string='Get favorites from this screen name',
        help="Screen Name of the Twitter Account from "
        "which you want to load favorites.",
        required=True
    )
    feed_length = fields.Integer(
        string='Number of tweets to show on the website'
    )
    base_twitter_api_path = fields.Char(
        string='Base twitter API path',
        default="https://api.twitter.com/1.1/"
    )

    theme = fields.Many2one(
        string="Default Theme for feed",
        comodel_name='twitter.theme',
        help="Default Theme, if the user does not select it "
             "from the widget it is the fallback for this feed",
        required=True
    )

    def get_token(self, c_key, c_secret):
        url = 'https://api.twitter.com/oauth2/token'
        credentials = base64.b64encode(
                '%s:%s' % (
                    urllib.quote(c_key),
                    urllib.quote(c_secret),
                ))
        request = urllib2.Request(url, data='grant_type=client_credentials')
        request.add_header("Authorization", "Basic %s" % credentials)
        request.add_header(
            "Content-Type",
            "application/x-www-form-urlencoded;charset=UTF-8")
        response = urllib2.urlopen(request)
        response_str = response.read()
        response_dict = json.loads(response_str)
        return str(response_dict['access_token'])

    @api.model
    def get_userposts(self, feed):
        token = self.get_token(
            feed.twitter_api_key,
            feed.twitter_api_secret
        )
        args = {
            'screen_name': feed.twitter_screen_name,
            'count': feed.feed_length,
            }
        url = feed.base_twitter_api_path + \
            "statuses/user_timeline.json?%s" % urllib.urlencode(
                args
            )
        request = urllib2.Request(url)
        request.add_header(
          "Authorization",  "Bearer %s" % token
        )
        request.add_header(
            'content-type',
            'application/x-www-form-urlencoded;charset=UTF-8'
        )
        response = urllib2.urlopen(request)
        return response.read()

    @api.model
    def get_all_twitter_feeds(self):
        feeds = self.env['twitter.feed'].search([])
        for feed in feeds:
            userposts = self.get_userposts(feed)
            userposts_dict = json.loads(userposts)
            if userposts_dict:
                feed.clear_tweets()
                for item in userposts_dict:
                    tweet_formatted_text = item['text']
                    at_users = list(set(re.findall(
                        '(?<=@)\w+', tweet_formatted_text
                    )))
                    hashtags = list(set(re.findall(
                        '(?<=#)\w+', tweet_formatted_text
                    )))
                    for at_user in at_users:
                        tweet_formatted_text = tweet_formatted_text.replace(
                            '@'+at_user,
                            '<span color="' + feed.theme.twitter_at_color +
                            '">@' + at_user + '</span>'
                        )
                    for hashtag in hashtags:
                        tweet_formatted_text = tweet_formatted_text.replace(
                            '#'+hashtag,
                            '<span color="' +
                            feed.theme.twitter_hashtag_color +
                            '">#' + hashtag + '</span>'
                        )
                    tweet_dict = {
                        'text': tweet_formatted_text,
                        'author': item['user']['name'],
                        'tweet_create_date': item['created_at'],
                        'tweet_id': item['id'],
                        'feed_id': feed.id,
                        }
                    self.env['twitter.tweet'].create(tweet_dict)
                    for entity in item['entities']['user_mentions']:
                        entitydict = {
                            'twitter_user_id': entity['id'],
                            'twitter_user_name': entity['name'],
                            'twitter_user_screen_name': entity['screen_name'],
                            'mentions': 1,
                            'feed_id': feed.id,
                            }
                        exists = self.env['twitter.user'].search(
                            [('twitter_user_id', '=', entity['id']),
                             ('feed_id', '=', self.id)]
                        )
                        if exists:
                            exists[0].write({'mentions': exists.mentions + 1})
                        else:
                            self.env['twitter.user'].create(entitydict)

    def clear_tweets(self):
        # Proposal maybe not delete but "archive"
        old_tweets = self.env['twitter.tweet'].search(
            [('feed_id', '=', self.id)]
        )
        old_tweets.unlink()
        return True

    def get_tweets(self):
        return self.env['twitter.tweet'].search(
                [('feed_id', '=', self.id)],
                limit=self.feed_length
            )
