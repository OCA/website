# -*- coding: utf-8 -*-
# © 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp import exceptions


class TestWebsiteForumCensored(TransactionCase):

    def setUp(self):
        super(TestWebsiteForumCensored, self).setUp()
        self.phrase_obj = self.env['forum.censored.phrase']
        self.tag_obj = self.env['forum.tag']
        self.post_obj = self.env['forum.post']
        self.forum_obj = self.env['forum.forum']

    def test_create_write(self):
        frm = self.forum_obj.create({'name': 'frm1'})
        phrase = self.phrase_obj.create({'phrase': 'cool',
                                         'replacement': 'hot'
                                         })
        self.assertEquals(len(phrase), 1)
        tag = self.tag_obj.create({'name': 'cool',
                                   'forum_id': frm.id
                                   })
        self.assertEquals(tag.name, 'hot')
        post = self.post_obj.create({'name': 'cool',
                                     'content': 'cool',
                                     'forum_id': frm.id
                                     })
        self.assertEquals(post.name, 'hot')
        self.assertEquals(post.content, '<p>hot</p>')
        post.write({'name': 'cool', 'content': 'cool'})
        self.assertEquals(post.name, 'hot')
        self.assertEquals(post.content, '<p>hot</p>')
        with self.assertRaises(exceptions.ValidationError):
            self.phrase_obj.create({'phrase': '[',
                                    'replacement': 'hot'
                                    })
