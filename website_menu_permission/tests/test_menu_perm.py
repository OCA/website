# -*- coding: utf-8 -*-
# Copyright 2017 Simone Orsi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)
import odoo.tests.common as test_common


class TestMenuPerm(test_common.TransactionCase):

    def setUp(self):
        super(TestMenuPerm, self).setUp()
        self.group_logged = self.env.ref('base.group_portal')
        self.group_public = self.env.ref('base.group_public')
        user_model = self.env['res.users'].with_context(**{
            'no_reset_password': True,
            'mail_create_nosubscribe': True})
        self.user_public = user_model.create({
            'name': 'User 1 (test ref)',
            'login': 'testref_user_public',
            'email': 'testref_user_public@email.com',
            # make sure to have only portal group
            'groups_id': [(6, 0, [self.group_public.id])]
        })
        self.user_logged = user_model.create({
            'name': 'Public User',
            'login': 'publicuser',
            'email': 'publicuser@example.com',
            'groups_id': [(6, 0, [self.group_logged.id])]}
        )
        self.menu_model = self.env['website.menu']
        self.menu_item = self.menu_model.create({'name': 'Foo'})

    def test_menu_groups_default(self):
        self.assertIn(self.group_logged, self.menu_item.group_ids)
        self.assertIn(self.group_public, self.menu_item.group_ids)

    def test_menu_groups_update(self):
        # wipe groups and flags
        self.menu_item.with_context(ws_menu_skip_group_update=1).write({
            'group_ids': False,
            'user_logged': False,
            'user_not_logged': False,
        })
        self.menu_item.user_logged = True
        self.assertIn(self.group_logged, self.menu_item.group_ids)
        self.assertNotIn(self.group_public, self.menu_item.group_ids)
        self.menu_item.user_not_logged = True
        self.assertIn(self.group_logged, self.menu_item.group_ids)
        self.assertIn(self.group_public, self.menu_item.group_ids)
        self.menu_item.user_logged = False
        self.assertNotIn(self.group_logged, self.menu_item.group_ids)
        self.assertIn(self.group_public, self.menu_item.group_ids)
        self.menu_item.user_not_logged = False
        self.assertNotIn(self.group_logged, self.menu_item.group_ids)
        self.assertNotIn(self.group_public, self.menu_item.group_ids)

    def test_perm_default_all_can_view(self):
        model = self.menu_model.sudo(self.user_public.id)
        self.assertIn(
            self.menu_item,
            model.search([])
        )
        model = self.menu_model.sudo(self.user_logged.id)
        self.assertIn(
            self.menu_item,
            model.search([])
        )

    def test_perm_public_only_can_view(self):
        self.menu_item.write({
            'user_logged': False,
            'user_not_logged': True,
        })
        model = self.menu_model.sudo(self.user_public.id)
        self.assertIn(
            self.menu_item,
            model.search([])
        )
        model = self.menu_model.sudo(self.user_logged.id)
        self.assertNotIn(
            self.menu_item,
            model.with_context(foo=1).search([])
        )

    def test_perm_logged_only_can_view(self):
        self.menu_item.write({
            'user_logged': True,
            'user_not_logged': False,
        })
        model = self.menu_model.sudo(self.user_public.id)
        self.assertNotIn(
            self.menu_item,
            model.search([])
        )
        model = self.menu_model.sudo(self.user_logged.id)
        self.assertIn(
            self.menu_item,
            model.with_context(foo=1).search([])
        )
