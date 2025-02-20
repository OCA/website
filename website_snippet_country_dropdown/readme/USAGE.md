To extend this template you need to inherit `country_dropdown` template
and add your personal code.

The template have three input text:

1.  `no_country_field`: Field without code country.
2.  `country_code_field`: Field with only country code (read only)
3.  `complete_field`: Field with the previous two joined (hidden)

The name of the complete field is customizable when user insert the
snippet into a form element with the website editor.

## Development

You can call the reusable Qweb template called
`website_snippet_country_dropdown.country_dropdown` in your views to add
a sensible country-combined field, ideal for *VATs*.

The default country will be the first match among:

1.  Extract it from the `default_country` variable.
2.  Extract it from the first 2 letters of the `default_value` variable.
3.  The current user's country.
4.  The current website's company's country.
5.  The first country in the list.

All variables you can use to modify its behavior:

- `complete_field` to give it a name. Usually it will match the field
  name.
- `default_value` for the `complete_field`.
- `countries` as a `res.country` ORM recordset.
- `default_country` as a `res.country` record.
- `no_country_placeholder`.

You can view an example in `website_sale_checkout_country_vat` in
OCA/e-commerce.
