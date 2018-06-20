# Copyright 2016 LasLabs Inc.
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import HttpCase
from ..controllers.main import Website
import mock
import base64

imp_cont = 'odoo.addons.website_logo.controllers.main'
imp_req = '%s.request' % imp_cont


class StopTestException(Exception):
    pass


class TestLogo(HttpCase):

    def setUp(self):
        super(TestLogo, self).setUp()
        self.model_obj = self.env['res.company']
        self.cont_obj = Website()
        self.rec_id = self.env.ref('base.main_company')
        self.image_val = base64.b64encode('Test'.encode('utf-8'))

    def test_image_logo_get_domain(self):
        """ It should search for logo using defined domain """
        mk = mock.MagicMock()
        mk.execute.side_effect = StopTestException
        expect = 'Test'
        with self.assertRaises(StopTestException):
            self.cont_obj._image_logo_get(mk, domain=expect)
        args = mk.execute.call_args
        self.assertIn(
            'SELECT logo, write_date', args[0][0],
            'Website logo select not in query call. Got %s' % args[0][0],
        )
        self.assertEqual(
            (expect, ), args[0][1],
            'Domain not in query call. Expect %s, Got %s' % (
                (expect, ), args[0][1],
            ),
        )

    def test_image_logo_get_no_domain(self):
        """ It should search for logo without a domain """
        mk = mock.MagicMock()
        mk.execute.side_effect = StopTestException
        with self.assertRaises(StopTestException):
            self.cont_obj._image_logo_get(mk)
        args = mk.execute.call_args
        self.assertIn(
            'SELECT logo, write_date', args[0][0],
            'Website logo select not in query call.',
        )
        self.assertNotIn(
            'WHERE name =', args[0][0],
            'Name condition in query w/ no domain.',
        )

    def test_image_logo_fetch(self):
        """ Query result should be fetched """
        mk = mock.MagicMock()
        mk.fetchone.side_effect = StopTestException
        with self.assertRaises(StopTestException):
            self.cont_obj._image_logo_get(mk)

    @mock.patch('%s.io.BytesIO' % imp_cont)
    def test_image_logo_returns_fetch_io(self, str_mk):
        """ Successful query should return StringIO image """
        mk = mock.MagicMock()
        expect1, expect2 = self.image_val, 'Test2'
        mk.fetchone.return_value = [expect1, expect2]
        res = self.cont_obj._image_logo_get(mk)
        str_mk.assert_called_once_with(base64.b64decode(expect1))
        self.assertEqual((str_mk(), expect2), res)

    @mock.patch('%s.functools' % imp_cont)
    @mock.patch('%s.http' % imp_cont)
    @mock.patch('%s.io' % imp_cont)
    @mock.patch(imp_req)
    def test_default_on_exception(self, imp_mk, str_mk, http_mk, func_mk):
        """ It should send the default logo if there is an exception """
        with mock.patch('%s.registry' % imp_cont) as mk:
            cr_mk = mk.Registry().cursor().__enter__()
            cr_mk.execute.side_effect = Exception('Mock Exception')
            self.cont_obj.website_logo()
            func_mk.partial().assert_called_once_with('website_nologo.png')
