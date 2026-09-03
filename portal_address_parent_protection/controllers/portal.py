# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalParentProtection(CustomerPortal):
    def _is_child_address(self, partner_sudo, **kwargs):
        """Whether the edited address is, or is about to become, a child of a
        company that it is not itself.

        On creation ``partner_sudo`` is empty, and
        ``_complete_address_values()`` attaches the new address to the current
        customer's commercial partner, so the address is a child as well. The
        conditions mirror the ones core uses to rename the parent.

        Core does not rename the parent on creation today, but only as a side
        effect: ``res.partner.create()`` sets ``company_name`` to ``False`` in
        place on the very dict the rename block reads afterwards. Covering the
        creation path keeps the protection symmetric if that ever changes.
        """
        if partner_sudo:
            return partner_sudo != partner_sudo.commercial_partner_id
        commercial_partner = (
            request.env["res.partner"]
            ._get_current_partner(**kwargs)
            .commercial_partner_id
        )
        return commercial_partner.is_company

    def _create_or_update_address(self, partner_sudo, *args, **form_data):
        """Never let a child address rename its commercial partner.

        Core only drops ``company_name`` when the edited address exists and is
        not the current customer's own record (see
        ``_validate_address_values``), so a contact renames its parent company
        both through its own address form and through the creation form, where
        the field is merely rendered read-only. The value is dropped from the
        form data before it is parsed, hence before core reaches the
        ``parent_company.name = company_name`` assignment.
        """
        if self._is_child_address(partner_sudo, **form_data):
            form_data.pop("company_name", None)
        return super()._create_or_update_address(partner_sudo, *args, **form_data)
