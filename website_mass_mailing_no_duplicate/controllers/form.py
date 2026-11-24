from odoo.tools.misc import clean_context

from odoo.addons.website.controllers import form


class WebsiteForm(form.WebsiteForm):
    def insert_record(self, request, model, values, custom, meta=None):
        if model.model == "mailing.contact":
            request.update_context(
                **clean_context({"mailing_contact_from_website": True})
            )
        return super().insert_record(request, model, values, custom, meta=meta)
