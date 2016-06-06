# -*- coding: utf-8 -*-
# © 2015-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError
import mock

imp_model = \
    'openerp.addons.website_form_recaptcha.models.website_form_recaptcha'
imp_requests = '%s.requests' % imp_model


class TestCaptcha(TransactionCase):

    def setUp(self):
        super(TestCaptcha, self).setUp()
        self.model_obj = self.env['website.form.recaptcha']
        self.secret_key = self.env.ref(
            'website_form_recaptcha.recaptcha_key_secret'
        ).value
        self.validate_vars = 'T1', 'T2'

    @mock.patch(imp_requests)
    def test_post_with_proper_data(self, mk):
        mk.post.side_effect = StopIteration
        exp1, exp2 = self.validate_vars
        try:
            self.model_obj.action_validate(exp1, exp2)
        except StopIteration:
            pass
        mk.post.assert_called_once_with(self.model_obj.URL, data={
            'secret': self.secret_key,
            'response': exp1,
            'remoteip': exp2,
        })

    @mock.patch(imp_requests)
    def test_valid(self, mk):
        expect = {
            'success': True,
        }
        mk.post().json.return_value = expect
        self.assertTrue(self.model_obj.action_validate(
            *self.validate_vars
        ))

    @mock.patch(imp_requests)
    def test_known_error_raises(self, mk):
        expect = {
            'error-codes': ['missing-input-secret'],
        }
        mk.post().json.return_value = expect
        with self.assertRaises(ValidationError):
            self.model_obj.action_validate(*self.validate_vars)

    @mock.patch(imp_requests)
    def test_known_error_lookup(self, mk):
        expect = {
            'error-codes': ['missing-input-secret'],
        }
        mk.post().json.return_value = expect
        try:
            self.model_obj.action_validate(*self.validate_vars)
        except ValidationError as e:
            self.assertEqual(
                e[0], self.model_obj.ERROR_MAP[expect['error-codes'][0]]
            )

    @mock.patch(imp_requests)
    def test_unknown_error_lookup(self, mk):
        expect = {
            'error-codes': ['derp'],
        }
        mk.post().json.return_value = expect
        try:
            self.model_obj.action_validate(*self.validate_vars)
        except ValidationError as e:
            self.assertEqual(
                e[0], self.model_obj.ERROR_MAP[None]
            )

    @mock.patch(imp_requests)
    def test_no_success_raises(self, mk):
        expect = {
            'success': False,
        }
        mk.post().json.return_value = expect
        with self.assertRaises(ValidationError):
            self.model_obj.action_validate(*self.validate_vars)
