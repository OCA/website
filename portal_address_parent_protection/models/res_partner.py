# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _can_be_edited_by_current_customer(self, **kwargs):
        """Portal users may never edit a company or a commercial partner other
        than their own partner record.

        The check is anchored on the partner of the logged in user instead of
        ``_get_current_partner()``, because that method is overridden by
        ``website_sale`` to return the customer of the current cart. When the
        cart customer is the parent company (as done by
        ``website_sale_partner_sale_contact``), the core check considers the
        company to be the customer's own record and grants full edit rights on
        it. Public users are left to the core behaviour, as their own partner is
        the public one while the cart may legitimately point to the address they
        just created.
        """
        self.ensure_one()
        user = self.env.user
        if user.share and not user._is_public():
            own_partner = user.partner_id
            if self != own_partner and (
                self.is_company or self == self.commercial_partner_id
            ):
                return False
        return super()._can_be_edited_by_current_customer(**kwargs)

    def _fields_sync(self, values):
        """Do not propagate a portal user's own address up to its parent.

        A contact of type ``contact`` normally shares its parent's address, so
        core writes the new address on the parent (see ``_fields_sync``, section
        "To UPSTREAM"). A portal contact editing their personal address would
        therefore overwrite the address of the whole company.

        Only address driven synchronisation is skipped: when ``parent_id`` is
        part of the write, the contact is being (re)attached to a company, and
        core is left to initialise that company's address as usual.
        """
        user = self.env.user
        if (
            user.share
            and not user._is_public()
            and "parent_id" not in values
            and self.parent_id
            and self.type == "contact"
        ):
            address_fields = self._address_fields()
            if any(fname in values for fname in address_fields):
                values = {
                    fname: value
                    for fname, value in values.items()
                    if fname not in address_fields
                }
        return super()._fields_sync(values)
