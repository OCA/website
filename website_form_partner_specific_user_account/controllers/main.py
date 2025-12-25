# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.website.controllers.form import WebsiteForm


class WebsiteForm(WebsiteForm):
    def insert_record(self, request, model, values, custom, meta=None):
        website = request.website
        if not website.specific_user_account:
            return super().insert_record(request, model, values, custom, meta)
        partner_id = values.get("partner_id")
        if not partner_id:
            return super().insert_record(request, model, values, custom, meta)
        Partner = request.env["res.partner"].sudo()
        partner = Partner.browse(partner_id)
        if not partner:
            return super().insert_record(request, model, values, custom, meta)
        email = (
            values.get("email_from")
            or values.get("partner_email")
            or values.get("email")
        )
        restrict = website.restrict_partner_to_company
        website_company = website.company_id
        # Conflicts based on what the partner already has
        company_conflict = (
            restrict
            and bool(partner.company_id)
            and partner.company_id != website_company
        )
        website_conflict = bool(partner.website_id) and partner.website_id != website
        # If there is any conflict, do not assign missing fields to this partner.
        # Instead, look for/create a partner that matches website (+company if restricted).
        if email and (website_conflict or company_conflict):
            domain = [
                ("email", "=", email),
                ("website_id", "=", website.id),
            ]
            if website.restrict_partner_to_company:
                domain.append(("company_id", "=", website.company_id.id))
            website_partner = Partner.search(domain, limit=1)
            if not website_partner:
                vals = {
                    "email": email,
                    "name": values.get("partner_name", False),
                    "website_id": website.id,
                }
                if website.restrict_partner_to_company:
                    vals["company_id"] = website.company_id.id
                website_partner = Partner.create(vals)
            values["partner_id"] = website_partner.id
            partner = website_partner
        # Intended for newly created partners, but applies to any partner without website_id
        if not partner.website_id:
            partner.website_id = website.id
        # Intended for newly created partners, but applies to any partner without company_id
        if restrict and not partner.company_id:
            partner.company_id = website_company.id
        return super().insert_record(request, model, values, custom, meta)
