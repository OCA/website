# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.fields import Date
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import ValidationError
from odoo.http import local_redirect, request, route
from odoo.osv.expression import AND, OR


_logger = logging.getLogger(__name__)


class ContactsCustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        Partner = request.env["res.partner"]
        if "contact_count" in counters:
            values["contact_count"] = Partner.search_count(self._contacts_domain())
        return values

    def _contacts_domain(self):
        """Get user's contacts domain."""
        partner = request.env.user.partner_id
        Partner = request.env["res.partner"]
        domain = [("type", "=", "contact"), ("active", "=", True)]
        domain += request.env.ref(
            "website_portal_contact.rule_edit_own_contacts"
        )._compute_domain("res.partner", "read")

        # To edit yourself you have /my/account
        domain += [("id", "!=", request.env.user.partner_id.id)]
        return domain

    def _get_archive_groups(
        self,
        model,
        domain=None,
        fields=None,
        groupby="create_date",
        order="create_date desc",
    ):
        if not model:
            return []
        if domain is None:
            domain = []
        if fields is None:
            fields = ["name", "create_date"]
        groups = []
        for group in request.env[model].read_group(
            domain, fields=fields, groupby=groupby, orderby=order
        ):
            label = group[groupby]
            date_begin = date_end = None
            for leaf in group["__domain"]:
                if leaf[0] == groupby:
                    if leaf[1] == ">=":
                        date_begin = leaf[2]
                    elif leaf[1] == "<":
                        date_end = leaf[2]
            groups.append(
                {
                    "date_begin": Date.to_string(Date.from_string(date_begin)),
                    "date_end": Date.to_string(Date.from_string(date_end)),
                    "name": label,
                    "item_count": group[groupby + "_count"],
                }
            )
        return groups

    def _get_contact_search_domain(self, search_in, search):
        search_domain = []
        if search_in in ("all"):
            search_domain = OR(
                [
                    search_domain,
                    [
                        "|",
                        "|",
                        ("name", "ilike", search),
                        ("mobile", "ilike", search),
                        ("email", "ilike", search),
                    ],
                ]
            )
        return search_domain

    def _prepare_contacts_values(
        self, page=1, date_begin=None, date_end=None, search="", search_in="all"
    ):
        """Prepare the rendering context for the contacts list."""
        values = self._prepare_portal_layout_values()
        Partner = request.env["res.partner"]
        base_url = "/my/contacts"

        # Get the required domains
        domain = self._contacts_domain()
        archive_groups = self._get_archive_groups("res.partner", domain)

        searchbar_inputs = {
            "all": {"input": "all", "label": _("Search in All")},
        }

        if search and search_in:
            domain += self._get_contact_search_domain(search_in, search)

        if date_begin and date_end:
            domain += [
                ("create_date", ">=", date_begin),
                ("create_date", "<", date_end),
            ]

        # Make pager
        pager = request.website.pager(
            url=base_url,
            url_args={"date_begin": date_begin, "date_end": date_end},
            total=Partner.search_count(domain),
            page=page,
            step=self._items_per_page,
        )

        # Current records to display
        contacts = Partner.search(
            domain, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_contacts_history"] = contacts.ids[:100]

        values.update(
            {
                "date": date_begin,
                "contacts": contacts,
                "total_contacts": len(contacts),
                "page_name": "contact",
                "pager": pager,
                "archive_groups": archive_groups,
                "default_url": base_url,
                "search": search,
                "search_in": search_in,
                "searchbar_inputs": searchbar_inputs,
            }
        )
        return values

    def _contacts_fields(self):
        """Fields to display in the form."""
        return [
            "name",
            "phone",
            "mobile",
            "email",
        ]

    def _contacts_fields_check(self, received):
        """Check received fields match those available."""
        disallowed = set(received) - set(self._contacts_fields())
        if disallowed:
            raise ValidationError(_("Fields not available: %s") % ", ".join(disallowed))

    def _contacts_clean_values(self, values):
        """Set values to a write-compatible format"""
        result = {k: v or False for k, v in values.items()}
        result.setdefault("type", "contact")
        result.setdefault("parent_id", request.env.user.commercial_partner_id.id)
        return result

    @http.route(
        ["/my/contacts", "/my/contacts/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_contacts(
        self, page=1, date_begin=None, date_end=None, search="", search_in="all", **kw
    ):
        values = self._prepare_contacts_values(page, date_begin, date_end, search)
        return request.render("website_portal_contact.portal_my_contacts", values)

    @http.route("/my/contacts/new", auth="user", website=True)
    def portal_my_contacts_new(self):
        """Form to create a contact."""
        contact = request.env["res.partner"].new()
        values = self._prepare_portal_layout_values()
        values.update(
            {
                "contact": contact,
                "page_name": "add_contact",
                "fields": self._contacts_fields(),
            }
        )
        return request.render("website_portal_contact.portal_my_contact", values)

    @http.route("/my/contacts/create", auth="user", website=True)
    def portal_my_contacts_create(self, redirect="/my/contacts/{}", **kwargs):
        """Create a contact."""
        Partner = request.env["res.partner"]
        self._contacts_fields_check(kwargs.keys())
        values = self._contacts_clean_values(kwargs)
        _logger.debug("Creating contact with: %s", values)
        contact = Partner.sudo().create(values)
        return local_redirect(redirect.format(contact.id))

    @http.route("/my/contacts/<int:contact>", type="http", auth="public", website=True)
    def portal_my_contacts_read(self, contact=None, access_token=None, **kw):
        """Read a contact form."""
        try:
            contact_sudo = self._document_check_access(
                "res.partner", contact, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        values = self._contact_get_page_view_values(contact_sudo, access_token, **kw)
        return request.render("website_portal_contact.portal_my_contact", values)

    # ------------------------------------------------------------
    # My Contact
    # ------------------------------------------------------------
    def _contact_get_page_view_values(self, contact, access_token, **kwargs):
        values = {
            "page_name": "contact",
            "contact": contact,
            "fields": self._contacts_fields(),
        }
        return self._get_page_view_values(
            contact, access_token, values, "my_contacts_history", False, **kwargs
        )

    @http.route("/my/contacts/<int:contact>/update", auth="user", website=True)
    def portal_my_contacts_update(self, contact, redirect="/my/contacts/{}", **kwargs):
        """Update a contact."""
        contact = request.env["res.partner"].browse(int(contact))
        self._contacts_fields_check(kwargs.keys())
        values = self._contacts_clean_values(kwargs)
        _logger.debug("Updating %r with: %s", contact, values)
        contact.write(values)
        return local_redirect(redirect.format(contact.id))

    @http.route("/my/contacts/<int:contact>/disable", auth="user", website=True)
    def portal_my_contacts_disable(self, contact, redirect="/my/contacts"):
        """Disable a contact."""
        contact = request.env["res.partner"].browse(int(contact))
        _logger.debug("Disabling %r", contact)
        contact.sudo().active = False
        return local_redirect(redirect)
