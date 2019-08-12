# Copyright 2017 Simone Orsi.
# Copyright 2019 Therp BV <https://therp.nl>.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
import odoo.tests.common as test_common


class TestMenuPerm(test_common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(
            cls.env.context, tracking_disable=True, no_reset_password=True))
        cls.group_portal = cls.env.ref('base.group_portal')
        cls.group_user = cls.env.ref('base.group_user')
        cls.group_public = cls.env.ref('base.group_public')
        user_model = cls.env['res.users'].with_context(**{
            'no_reset_password': True,
            'mail_create_nosubscribe': True})
        cls.employee_user = user_model.create({
            'name': 'Employee user (test ref)',
            'login': 'testref_employee_user',
            'email': 'testref_employee_user@email.com',
            'groups_id': [(6, 0, [cls.group_user.id])]})
        cls.portal_user = user_model.create({
            'name': 'Portal user',
            'login': 'portaluser',
            'email': 'portaluser@example.com',
            'groups_id': [(6, 0, [cls.group_portal.id])]})
        cls.public_user = cls.env.ref('base.public_user')
        cls.menu_model = cls.env['website.menu']
        cls.menu_item = cls.menu_model.create({'name': 'Foo'})

    def test_menu_for_all(self):
        self.menu_item.write({'group_ids': False})
        self.assertTrue(self._can_see(self.employee_user))
        self.assertTrue(self._can_see(self.public_user))
        self.assertTrue(self._can_see(self.portal_user))

    def test_menu_for_employee(self):
        self.menu_item.write({'group_ids': [(6, 0, [self.group_user.id])]})
        self.assertTrue(self._can_see(self.employee_user))
        self.assertFalse(self._can_see(self.public_user))
        self.assertFalse(self._can_see(self.portal_user))

    def test_menu_for_external(self):
        self.menu_item.write({'group_ids': [(6, 0, [self.group_portal.id])]})
        self.assertFalse(self._can_see(self.employee_user))
        self.assertFalse(self._can_see(self.public_user))
        self.assertTrue(self._can_see(self.portal_user))

    def test_menu_for_logged_in_users(self):
        self.menu_item.write(
            {'group_ids': [(6, 0, [
                self.group_portal.id, self.group_user.id])]})
        self.assertTrue(self._can_see(self.employee_user))
        self.assertFalse(self._can_see(self.public_user))
        self.assertTrue(self._can_see(self.portal_user))

    def test_menu_for_not_logged_in_users(self):
        self.menu_item.write({'group_ids': [(6, 0, [self.group_public.id])]})
        self.assertFalse(self._can_see(self.employee_user))
        self.assertTrue(self._can_see(self.public_user))
        self.assertFalse(self._can_see(self.portal_user))

    def test_menu_for_all_explicit(self):
        self.menu_item.write(
            {'group_ids': [(6, 0, [
                self.group_portal.id,
                self.group_user.id,
                self.group_public.id])]})
        self.assertTrue(self._can_see(self.employee_user))
        self.assertTrue(self._can_see(self.public_user))
        self.assertTrue(self._can_see(self.portal_user))

    def _can_see(self, user):
        """Check wether user can see the test menu."""
        menu_model_sudo = self.menu_model.sudo(user.id)
        can_see = self.menu_item in menu_model_sudo.search([])
        return can_see
