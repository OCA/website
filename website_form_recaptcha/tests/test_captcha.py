# Copyright 2015-2017 LasLabs Inc.
# Copyright 2019 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import mock

imp_model = \
    'odoo.addons.website_form_recaptcha.models.website_form_recaptcha'
imp_requests = '%s.requests' % imp_model


class TestCaptcha(TransactionCase):

    def setUp(self):
        super(TestCaptcha, self).setUp()
        self.model_obj = self.env['website.form.recaptcha']
        self.secret_key = self.env.ref(
            'website_form_recaptcha.recaptcha_key_secret'
        ).value
        self.validate_vars = 'T1', 'T2'
        self.website = self.env['website'].search([], limit=1)

    @mock.patch(imp_requests)
    def test_post_with_proper_data(self, mk):
        mk.post.side_effect = StopIteration
        exp1, exp2 = self.validate_vars
        try:
            self.model_obj.validate_response(exp1, exp2, website=self.website)
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
        self.assertTrue(self.model_obj.validate_response(
            *self.validate_vars, website=self.website
        ))

    @mock.patch(imp_requests)
    def test_known_error_raises(self, mk):
        expect = {
            'error-codes': ['missing-input-secret'],
        }
        mk.post().json.return_value = expect
        with self.assertRaises(ValidationError):
            self.model_obj.validate_response(
                *self.validate_vars, website=self.website)

    @mock.patch(imp_requests)
    def test_known_error_lookup(self, mk):
        expect = {
            'error-codes': ['missing-input-secret'],
        }
        mk.post().json.return_value = expect
        try:
            self.model_obj.validate_response(
                *self.validate_vars, website=self.website)
        except ValidationError as e:
            self.assertEqual(
                e.name,
                self.model_obj._get_error_message(expect['error-codes'][0])
            )

    @mock.patch(imp_requests)
    def test_unknown_error_lookup(self, mk):
        expect = {
            'error-codes': ['derp'],
        }
        mk.post().json.return_value = expect
        try:
            self.model_obj.validate_response(
                *self.validate_vars, website=self.website)
        except ValidationError as e:
            self.assertEqual(
                e.name, self.model_obj._get_error_message()
            )

    @mock.patch(imp_requests)
    def test_no_success_raises(self, mk):
        expect = {
            'success': False,
        }
        mk.post().json.return_value = expect
        with self.assertRaises(ValidationError):
            self.model_obj.validate_response(
                *self.validate_vars, website=self.website)

    def test_get_credentials(self):
        # by default retrieve global value from config params
        creds = self.model_obj._get_api_credentials(website=self.website)
        self.assertEqual(creds, {
            'site_key': 'Obtain from Google',
            'secret_key': 'Obtain from Google',
        })
        # customize on the website
        self.website.write({
            'recaptcha_key_site': '1234567890',
            'recaptcha_key_secret': '0123456789',
        })
        creds = self.model_obj._get_api_credentials(website=self.website)
        self.assertEqual(creds, {
            'site_key': '1234567890',
            'secret_key': '0123456789',
        })
