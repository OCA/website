# -*- coding: utf-8 -*-
"""Base Controller of all controllers for a single form page."""
# Copyright 2019 - Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _
from odoo.exceptions import ValidationError

from . import BaseFormHandler


class ExampleFormHandler(BaseFormHandler):
    """This class is an example handler for form pages.

    It lets the user enter a number between 1 and 10, shows validation and
    error handling, and going to the next page (the home url '/' in this case)
    on success.
    """
    _form_template = 'wnb_website.template_example_form'

    def load_form(self):
        """Load extra data needed to render the form."""
        self.qcontext['display_name'] = \
            _('Guest') if self.is_public else \
            self.request.env.user.partner_id.display_name

    def validate_form(self):
        """Validate user input on the form. Return array of errors."""
        super(ExampleFormHandler, self).validate_form()
        test_number = self.qcontext.get('test_number', "0")
        try:
            number = int(test_number)
        except Exception:  # pylint: disable=broad-except
            raise ValidationError(
                _("%s is not a number") % test_number)
        if number < 1 or number > 9:
            raise ValidationError(
                _("%d is not between 1 and 10") % number)
