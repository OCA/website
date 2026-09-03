- `website_event_sale` calls `CustomerPortal()._create_or_update_address()` on
  the core class instead of on the extended controller, so the `company_name`
  protection does not apply to the event registration form. The edit right and
  address synchronisation protections, which live on `res.partner`, still do.
- When the company address is incomplete, portal users can no longer complete it
  themselves. Core accounts for this: `website_sale` only redirects to the
  address form for addresses the customer may edit, so the checkout is not
  interrupted.
- On the address creation path the `company_name` protection is defensive only.
  Core does not rename the parent there, but as a side effect of
  `res.partner.create()` blanking `company_name` in place on the values the
  rename block reads afterwards.
