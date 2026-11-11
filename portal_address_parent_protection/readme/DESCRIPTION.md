A portal user who is a child contact of a company can rename that company, and
overwrite its address, from the frontend address forms. This module closes the
three paths that allow it.

Renaming the company. Core drops the `company_name` value only when the edited
address is not the current customer's own record, so a contact renames its
parent company through its own address form.

Editing the company itself. `_can_be_edited_by_current_customer()` compares the
edited record with `_get_current_partner()`, which `website_sale` overrides to
return the customer of the current cart. When something sets that customer to
the parent company - `website_sale_partner_sale_contact` does exactly that -
core considers the company to be the customer's own record and grants full edit
rights on it during checkout: name, email, phone and address.

Overwriting the company address. A contact of type `contact` shares its parent's
address, so core propagates any address change up to the parent
(`res.partner._fields_sync()`). A portal contact saving their personal address
therefore replaces the address of the whole company.
