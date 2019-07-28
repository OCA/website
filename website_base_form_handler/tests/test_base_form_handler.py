# -*- coding: utf-8 -*-
"""Test base form handler and example controller."""
# Copyright 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=missing-docstring,no-self-use,too-few-public-methods
from odoo.tests.common import TransactionCase

from ..controllers.handlers import ExampleFormHandler


class FakeHttpRequest(object):

    def __init__(self, method):
        self.remote_address = None
        self.headers = {}
        self.method = method  # GET or POST


class FakeRequest(object):

    def __init__(self, httprequest, env):
        self.httprequest = httprequest
        self.env = env

    def redirect(self, url):
        return url

    def render(self, template, qcontext):
        return {'template': template, 'qcontext': qcontext}


class ExampleHandlerCase(TransactionCase):

    def test_get(self):
        """Calling GET on example handler should result in right template."""
        request = FakeRequest(FakeHttpRequest('GET'), self.env)
        result = ExampleFormHandler(self, request, {}).handle_form()
        self.assertEqual(
            result['template'], 'wnb_website.template_example_form')

    def test_post_error(self):
        """Calling POST on example handler with wrong input."""
        request = FakeRequest(FakeHttpRequest('POST'), self.env)
        result = ExampleFormHandler(
            self, request, {'test_number': 'not a number'}).handle_form()
        self.assertEqual(
            result['template'], 'wnb_website.template_example_form')
        self.assertIn('error', result['qcontext'])

    def test_post_success(self):
        """Calling POST on example handler with correct input."""
        request = FakeRequest(FakeHttpRequest('POST'), self.env)
        result = ExampleFormHandler(
            self, request, {'test_number': '9'}).handle_form()
        self.assertEqual(result, '/')
