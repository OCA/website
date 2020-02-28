# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from openerp import _
from openerp.addons.website_portal_v10.controllers.main \
    import WebsiteAccount as PortalController
from openerp.exceptions import ValidationError
from openerp.http import local_redirect, request, route

_logger = logging.getLogger(__name__)


class WebsiteAccount(PortalController):
    def _contacts_domain(self, search=""):
        """Get user's contacts domain."""
        domain = request.env.ref(
            "website_portal_contact.rule_edit_own_contacts").domain

        # To edit yourself you have /my/account
        domain += [("id", "!=", request.env.user.partner_id.id)]

        # Add search query
        for term in search.split():
            domain += [
                "|", "|",
                ("name", "ilike", term),
                ("mobile", "ilike", term),
                ("email", "ilike", term),
            ]

        return domain

    def _prepare_contacts_values(self, page=1, date_begin=None, date_end=None,
                                 search=""):
        """Prepare the rendering context for the contacts list."""
        values = self._prepare_portal_layout_values()
        Partner = request.env["res.partner"]
        base_url = "/my/contacts"

        # Get the required domains
        domain = self._contacts_domain(search)
        archive_groups = self._get_archive_groups("res.partner", domain)

        if date_begin and date_end:
            domain += [("create_date", ">=", date_begin),
                       ("create_date", "<", date_end)]

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
            domain, limit=self._items_per_page, offset=pager["offset"])

        values.update({
            "date": date_begin,
            "contacts": contacts,
            "pager": pager,
            "archive_groups": archive_groups,
            "default_url": base_url,
            "search": search,
        })

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
            raise ValidationError(
                _("Fields not available: %s") % ", ".join(disallowed))

    def _contacts_clean_values(self, values):
        """Set values to a write-compatible format"""
        result = {k: v or False for k, v in values.iteritems()}
        result.setdefault("type", "contact")
        result.setdefault(
            "parent_id", request.env.user.commercial_partner_id.id)
        return result

    @route()
    def account(self, *args, **kwargs):
        result = super(WebsiteAccount, self).account(*args, **kwargs)
        result.qcontext.update({
            "contact_count": request.env["res.partner"].search_count(
                self._contacts_domain())
        })
        return result

    @route(["/my/contacts", "/my/contacts/page/<int:page>"],
           auth="user", website=True)
    def portal_my_contacts(self, page=1, date_begin=None, date_end=None,
                           search=""):
        """List all of your contacts."""
        return request.website.render(
            "website_portal_contact.portal_my_contacts",
            self._prepare_contacts_values(page, date_begin, date_end, search))

    @route("/my/contacts/new",
           auth="user", website=True)
    def portal_my_contacts_new(self):
        """Form to create a contact."""
        return self.portal_my_contacts_read(request.env["res.partner"].new())

    @route("/my/contacts/create",
           auth="user", website=True)
    def portal_my_contacts_create(self, redirect="/my/contacts/{}", **kwargs):
        """Create a contact."""
        self._contacts_fields_check(kwargs.keys())
        values = self._contacts_clean_values(kwargs)
        _logger.debug("Creating contact with: %s", values)
        contact = request.env["res.partner"].create(values)
        return local_redirect(redirect.format(contact.id))

    @route("/my/contacts/<model('res.partner'):contact>",
           auth="user", website=True)
    def portal_my_contacts_read(self, contact):
        """Read a contact form."""
        values = self._prepare_portal_layout_values()
        values.update({
            "contact": contact,
            "fields": self._contacts_fields(),
        })
        return request.website.render(
            "website_portal_contact.contacts_followup", values)

    @route("/my/contacts/<model('res.partner'):contact>/update",
           auth="user", website=True)
    def portal_my_contacts_update(self, contact, redirect="/my/contacts/{}",
                                  **kwargs):
        """Update a contact."""
        self._contacts_fields_check(kwargs.keys())
        values = self._contacts_clean_values(kwargs)
        _logger.debug("Updating %r with: %s", contact, values)
        contact.write(values)
        return local_redirect(redirect.format(contact.id))

    @route("/my/contacts/<model('res.partner'):contact>/disable",
           auth="user", website=True)
    def portal_my_contacts_disable(self, contact, redirect="/my/contacts"):
        """Disable a contact."""
        _logger.debug("Disabling %r", contact)
        contact.sudo().active = False
        return local_redirect(redirect)
