# -*- coding: utf-8 -*-
"""Base Controller of all controllers for a single form page."""
# Copyright 2019 - Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=no-self-use,protected-access
import logging
from datetime import datetime

from odoo import _, fields
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class BaseFormHandler(object):
    """This class is a base handler for form pages.

    It handles the basic logic of a form, for both the GET and the POST
    requests:
    - loading the form data;
    - rendering the form;
    - validating the post;
    - if needed, reload the form with error-information;
    - on successfulll handling of a post, lead the user to the next step.

    Generally encountered arguments / variables:
    qcontext : the data passed to render a template / prefill a form.
               We will qcontext always have a superset of the keys in kw, so
               it is never needed to pass both qcontext and kw to functions.

    We will not whitelist any keys coming from website, except that updates
    will only ever be done with known keys/fieldnames.
    """
    _form_template = None

    def __init__(self, controller, request, qcontext):
        """Enable object wide variables."""
        self.controller = controller
        self.request = request
        self.qcontext = qcontext
        self.env = request.env
        public_user = self.env.ref('base.public_user')
        self.is_public = self.env.user == public_user
        self.sudo_env = public_user.sudo().env
        self.qcontext['is_public'] = self.is_public  # For use in templates.

    def handle_form(self):
        """This must be called from all subclasses."""
        if self.should_load_form():
            return self.handle_get()
        return self.handle_post()

    def should_load_form(self):
        """Wether we should load and display the form.

        This is true if we are handling a GET request, or when another handler
        has requested a load (basically an internal redirect).
        """
        if self.request.httprequest.method == 'GET':
            return True
        if self.qcontext.get('internal_redirect', False):
            self.qcontext.pop('internal_redirect')
            return True
        return False

    def handle_get(self):
        """Handle GET requests (can also be internal redirects)."""
        self.initial_load_form()
        return self.display_form()

    def handle_post(self):
        """Handle POST request."""
        try:
            self.validate_form()
            self.update_from_form()
            # Update was succesfull, on to next page.
            self.qcontext['internal_redirect'] = True
            return self.next_step()
        except ValidationError as error:
            self.handle_validation_error(error)
        except Exception:  # pylint: disable=broad-except
            self.handle_exception()
        return self.display_form()

    def initial_load_form(self):
        """Load data for first rendering of form.

        This might be called to load values from the database.
        """
        pass

    def display_form(self):
        """Display page, or redisplay after validation."""
        self.load_form()
        return self.render_form()

    def load_form(self):
        """Load data needed to render the form.

        This will be called before each rendering of the form.
        """
        pass

    def render_form(self):
        """Render the form template."""
        return self.render(self._form_template)

    def validate_form(self):
        """Validate user input on the form.

        This method shourd throw a ValidationError when the form does
        not pass validation
        """
        pass

    def update_from_form(self):
        """Update back-end with form data.i

        Make sure to only use data that we know should have been in the form.
        """
        pass

    def next_step(self):
        """Where to go after succesfull page submission."""
        return self.request.redirect('/')

    def render(self, template):
        """Render template, might be any, with present qcontext."""
        return self.request.render(template, self.qcontext)

    def handle_validation_error(self, error):
        """For the moment we only handle single errors."""
        self.set_error(
            _("Please correct your input: %s") % error.name)

    def handle_exception(self):
        """Log detailed exception, but give general message to user."""
        _logger.exception(
            _("Error on update or next step from form %s"),
            self._form_template)
        self.set_error(
            _("An unexpected error occured."
              " Try again later or contact the website owner"))

    def set_error(self, message):
        """Store error in context for display on form."""
        self.qcontext['error'] = message

    def set_default_value(self, values, key, default):
        """Set default value, if value not yet present."""
        if key in values:
            return
        values[key] = default

    def move_data(self, source=None, sink=None, keys=None):
        """Move data from source to sink.

        Might be used to move record data to qcontext,
        or the other way around.
        """
        for key in keys:
            if key in source:
                sink[key] = source[key]

    def convert_date_to_server_format(self, input_date):
        """Convert a date formatted according to user locale to server locale.

        Parameters
        ----------
        input_date:
            A date string coming from a form.
            The datepicker now inserts the date in the current
            locale format of the user.

        @returns: the date in standard odoo server format.
        """
        input_date_date = datetime.strptime(
            input_date, self.request.env['res.lang']._lang_get(
                self.request.env.user.lang).date_format)
        return fields.Date.to_string(input_date_date)
