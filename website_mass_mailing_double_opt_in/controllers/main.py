import uuid

from odoo.http import Controller, request, route

from odoo.addons.mass_mailing.controllers.main import MassMailController


class MassMailController(MassMailController):
    @route("/website_mass_mailing/subscribe", type="json", website=True, auth="public")
    def subscribe(self, list_id, email, **post):
        Contacts = request.env["mailing.contact"].sudo()
        if not request.env["ir.http"]._verify_request_recaptcha_token(
            "website_mass_mailing_double_opt_in"
        ):
            return {
                "toast_type": "danger",
                "toast_content": ("Suspicious activity detected by Google reCaptcha."),
            }
        ContactSubscription = request.env["mailing.contact.subscription"].sudo()
        name, email = Contacts.get_name_email(email)
        if request.lang.code == "de_DE":
            list_id = request.env.ref(
                "website_mass_mailing_double_opt_in.german_newsletter_mass_mail_list"
            ).id
        existing_contact = Contacts.search(
            [("list_ids", "=", int(list_id)), ("email", "=", email)], limit=1
        )
        mailing_list_contact = None
        if not existing_contact:
            # inline add_to_list as we've already called half of it
            contact_id = Contacts.search([("email", "=", email)], limit=1)
            if not contact_id:
                contact_id = Contacts.create(
                    {"name": name, "email": email, "opt_out": True}
                )
                mailing_list_contact = contact_id.subscription_list_ids.filtered(
                    lambda c: c.list_id.id == int(list_id)
                )
            ContactSubscription.create(
                {"contact_id": contact_id.id, "list_id": list_id}
            )
        elif existing_contact.opt_out:
            existing_contact.opt_out = False
        if mailing_list_contact:
            mail_language = request.lang
            if post.get("language"):
                mail_language = post.get("language")
            mailing_list_contact.write(
                {
                    "opt_out": True,
                    "access_token": str(uuid.uuid4().hex),
                    "mail_language": mail_language,
                }
            )
            template = request.env.ref(
                "website_mass_mailing_double_opt_in.newsletter_confirmation_request_template"
            ).sudo()
            template.with_context(lang=mail_language).send_mail(
                mailing_list_contact.id, force_send=True
            )
        # add email to session
        request.session["mass_mailing_email"] = email
        return {
            "toast_type": "success",
            "toast_content": ("Thanks for subscribing!"),
        }


class ConsentController(Controller):
    @route("/subscribed", type="http", auth="user", website=True)
    def subscribed(self, **kwargs):
        return request.render("website_mass_mailing_double_opt_in.subscribe")

    @route(
        "/newsletter/confirmation/<access_token>",
        type="http",
        auth="none",
        website=True,
    )
    def consent(self, access_token, **kwargs):
        mailing_list_contact = (
            request.env["mailing.contact.subscription"]
            .sudo()
            .search([("access_token", "=", access_token)])
        )
        if mailing_list_contact:
            mailing_list_contact.write({"opt_out": False})
            template = request.env.ref(
                "website_mass_mailing_double_opt_in.newsletter_confirmation_success_template"
            ).sudo()
            template.with_context(lang=mailing_list_contact.mail_language).send_mail(
                mailing_list_contact.id, force_send=True
            )
            base_url = request.httprequest.base_url
            base_url += "/subscribed"
            return request.redirect(base_url)
        else:
            return request.render(
                "website_mass_mailing_double_opt_in.invalid_subscription_confirmation_template"
            )
