# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalCopyOnEdit(CustomerPortal):
    def _address_must_be_copied(self, partner_sudo, address_values):
        """Whether the submitted values must create a new address.

        Only the additional addresses of a portal customer are copied. The
        customer's own contact record is edited in place: it is not an invoice
        or delivery address, it is their own data, and replacing it would
        detach them from their documents.

        Values that changed nothing are not copied either, so opening an
        address and saving it untouched does not leave a duplicate behind.
        """
        if not partner_sudo:
            return False
        user = request.env.user
        if not user.share or user._is_public():
            return False
        if partner_sudo == user.partner_id:
            return False
        if partner_sudo.type not in ("invoice", "delivery", "other"):
            return False
        return not self._are_same_addresses(address_values, partner_sudo)

    def _create_or_update_address(self, partner_sudo, *args, **form_data):
        """Create a new address instead of writing on the edited one.

        Documents are issued with the address as it was, so editing it in
        place rewrites what past orders, invoices and delivery notes display.

        Core creates a new address whenever no partner is given, and the
        caller uses the returned record, so dropping the partner is enough:
        the new address is completed and attached to the commercial partner
        by ``_complete_address_values()``, and the cart is repointed to it by
        ``website_sale``.
        """
        address_values, _extra_form_data = self._parse_form_data(form_data)
        if self._address_must_be_copied(partner_sudo, address_values):
            partner_sudo = request.env["res.partner"]
        return super()._create_or_update_address(partner_sudo, *args, **form_data)
