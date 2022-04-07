# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import _
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import ValidationError
from odoo.http import local_redirect, request, route

_logger = logging.getLogger(__name__)


class WebsiteAccount(CustomerPortal):
    def _contacts_domain(self, search=""):
        """Get user's contacts domain."""
        partner = request.env.user.partner_id
        domain = [
            ('id', 'child_of', partner.id)
        ]

        # To edit yourself you have /my/account
        domain += [("id", "!=", partner.id)]

        # Add search query
        for term in search.split():
            domain += [
                "|",
                "|",
                ("name", "ilike", term),
                ("mobile", "ilike", term),
                ("email", "ilike", term),
            ]

        return domain

    def _prepare_portal_layout_values(self, contact=None):
        values = super(WebsiteAccount, self)._prepare_portal_layout_values()
        partner_counts = request.env["res.partner"].search_count(
            self._contacts_domain()
        )
        values['contact_count'] = partner_counts
        return values

    def _prepare_contacts_values(
        self, page=1, date_begin=None, date_end=None, search="", sortby=None
    ):
        """Prepare the rendering context for the contacts list."""
        values = self._prepare_portal_layout_values()
        Partner = request.env["res.partner"]
        base_url = "/my/contacts"

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # Get the required domains
        domain = self._contacts_domain(search)
        archive_groups = self._get_archive_groups("res.partner", domain)

        if date_begin and date_end:
            domain += [
                ("create_date", ">=", date_begin),
                ("create_date", "<", date_end),
            ]

        # Make pager
        pager = request.website.pager(
            url=base_url,
            url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
            total=Partner.search_count(domain),
            page=page,
            step=self._items_per_page,
        )

        # Current records to display
        contacts = Partner.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session['my_contacts_history'] = contacts.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "contacts": contacts,
                "page_name": 'contact',
                "pager": pager,
                "archive_groups": archive_groups,
                "default_url": base_url,
                "search": search,
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby
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
            raise ValidationError(
                _("Fields not available: %s") % ", ".join(disallowed)
            )

    def _contacts_clean_values(self, values, contact=False):
        """Set values to a write-compatible format"""
        result = {k: v or False for k, v in values.items()}
        result.setdefault("type", "contact")
        user_partner = request.env.user.partner_id
        if not contact:
            # Contact creation
            result.setdefault(
                "parent_id", user_partner.id
            )
        return result

    @route(
        ["/my/contacts", "/my/contacts/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_contacts(
        self, page=1, date_begin=None, date_end=None, sortby=None, search="", **kw
    ):
        """List all of your contacts."""
        values = self._prepare_contacts_values(page, date_begin, date_end, search,
                                               sortby)
        return request.render("website_portal_contact.portal_my_contacts", values)

    @route("/my/contacts/new", auth="user", website=True)
    def portal_my_contacts_new(self):
        """Form to create a contact."""
        return self.portal_my_contacts_read(request.env["res.partner"].new())

    @route("/my/contacts/create", auth="user", website=True)
    def portal_my_contacts_create(self, redirect="/my/contacts", **kwargs):
        """Create a contact."""
        self._contacts_fields_check(kwargs.keys())
        values = self._contacts_clean_values(kwargs)
        _logger.debug("Creating contact with: %s", values)
        request.env["res.partner"].create(values)
        return local_redirect(redirect)

    def _contact_get_page_view_values(self, contact, access_token, **kwargs):
        values = {
            "contact": contact,
            "fields": self._contacts_fields(),
            'page_name': 'contact',
            'user': request.env.user
        }

        return self._get_page_view_values(contact, access_token, values,
                                          'my_contact_history', False, **kwargs)

    @route(
        ["/my/contacts/<model('res.partner'):contact>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_contacts_read(self, contact, access_token=None, **kw):
        """Read a contact form."""
        values = self._contact_get_page_view_values(contact, access_token, **kw)
        return request.render(
            "website_portal_contact.form", values
        )

    @route(
        "/my/contacts/<model('res.partner'):contact>/update",
        auth="user",
        website=True,
    )
    def portal_my_contacts_update(
        self, contact, redirect="/my/contacts", **kwargs
    ):
        """Update a contact."""
        self._contacts_fields_check(kwargs.keys())
        values = self._contacts_clean_values(kwargs, contact=contact)
        _logger.debug("Updating %r with: %s", contact, values)
        contact.write(values)
        return local_redirect(redirect)

    @route(
        "/my/contacts/<model('res.partner'):contact>/disable",
        auth="user",
        website=True,
    )
    def portal_my_contacts_disable(self, contact, redirect="/my/contacts"):
        """Disable a contact."""
        _logger.debug("Disabling %r", contact)
        contact.sudo().active = False
        return local_redirect(redirect)
