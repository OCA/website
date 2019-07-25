# -*- coding: utf-8 -*-
"""Example Controller to demonstrate use of handler classes."""
# Copyright 2019 - Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=too-few-public-methods,unused-argument
from odoo import http
from odoo.http import request

from .handlers import ExampleFormHandler


class ExampleFormController(http.Controller):
    """This class demonstrate how to use the handler classes from a controller.

    The class can not itself be used to derive ther controllers with standard
    method names, because controllers use the same extention mechanisme as
    Odoo models, so each subclass automatically overrides the methods of the
    superclass, which is not what we want in this case.
    """
    @http.route(
        '/example_form', type='http', auth='public', website=True)
    def example_form(self, *args, **kw):
        """Link the specific url to the common page handler.

        It is the responsibility of the method handling a request to convert
        the variable *args and keyword **kw arguments to a qcontext
        dictionary.
        """
        qcontext = dict(kw)
        handler = ExampleFormHandler(self, request, qcontext)
        return handler.handle_form()
