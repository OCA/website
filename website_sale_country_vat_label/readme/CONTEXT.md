### Business Need

In many countries, the term "VAT" (Value Added Tax) is not commonly used or recognized by local citizens and businesses. For instance, companies and customers in Chile look for "RUT", in Brazil for "CPF/CNPJ", in Spain for "NIF/CIF", and in the United States for "EIN". 

When an international or localized e-commerce website forces users to fill out a field labeled generically as "VAT", it creates friction and confusion during the checkout process. Users are often unsure whether they should enter their personal ID, corporate tax number, or if the field even applies to them. This module resolves this issue by automatically adapting the form terminology to match local expectations based on the selected country, thereby reducing cart abandonment and improving data quality at registration.

### Approach

This module extends the standard Odoo website address rendering controller. It intercepts the dictionary of values sent to the frontend address form template (`_prepare_address_form_values`) and dynamically replaces the static 'VAT' string label. It fetches the `vat_label` field configured on the selected country's backend record (`res.country`). If a specific label is defined for that country, it is displayed; otherwise, it seamlessly falls back to the standard "VAT" term.

### Useful Information

* **Dependencies:** This module directly extends `website_sale` (the core Odoo eCommerce module) and relies on the base `res.country` model features.
* **Recommended Setups:** 
  * **Multi-website:** Highly recommended for businesses running multiple localized websites targeting different regions or countries from a single Odoo database.
  * **B2B Portals:** Essential for companies with a heavy B2B focus where accurate tax identification is mandatory for automated invoicing.
* **Complementary Modules:** This module pairs perfectly with OCA localization modules (such as `l10n_br_website_sale` or equivalent local modules) that enforce specific tax validation rules, ensuring that the field not only looks right but also validates correctly according to local laws.