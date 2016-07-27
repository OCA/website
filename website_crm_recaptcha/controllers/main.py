# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.http import route
from openerp.exceptions import ValidationError
from openerp.addons.website_form_recaptcha.controllers.main import WebsiteForm
from openerp.addons.website_crm.controllers.main import contactus


class ContactUsRecaptcha(WebsiteForm, contactus):
    @route()
    def contactus(self, **kwargs):
        """Check ReCaptcha before creating the lead."""
        description, bad = kwargs.get("description"), False
        try:
            self.extract_data(**kwargs)
        except ValidationError:
            # Mock super() to make it fail by removing a required field
            kwargs.pop("description", None)
            bad = True

        result = super(ContactUsRecaptcha, self).contactus(**kwargs)
        if "error" in result.qcontext:
            # Restore the required field in the context
            if description:
                result.qcontext["description"] = description
                result.qcontext["error"].discard("description")

            # Record ReCaptcha failure
            if bad:
                result.qcontext["error"].add("recaptcha")

        return result
