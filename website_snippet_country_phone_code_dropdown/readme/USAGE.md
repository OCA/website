To extend this template, you should inherit the country_dropdown
template and add your custom code. This template includes three input
text fields, which are the following:

1.  `no_country_field`: Field without code country.
2.  `country_phone_code_field`: Field with only country code (read only)
3.  `complete_field`: Field with the previous two joined (hidden)

The name of the complete field is customizable when user insert the
snippet into a form element with the website editor.

## Development

In order to use this element, you can call the reusable Qweb template
website_snippet_country_phone_code_dropdown.country_dropdown in your
views or forms to add a sensible country-combined field, which could be
a useful element for the registration of international phone numbers.

**Default Country Selection**

The default country will be determined by the first match among:

1.  Extracted from the default_country variable.
2.  Extracted from the default_value_prefix variable, searching by phone
    code.
3.  The current user's country.
4.  The current website's company's country.
5.  The first country in the list.

**Variables**

All variables you can use to modify its behavior:

1.  `complete_field`: To give the form information a name. Habitually it
    will match the field name.
2.  `default_value_prefix`: The phone prefix to be used in the
    complete_field.
3.  `default_value_number`: The phone number to be used in the
    complete_field.
4.  `countries`: A recordset of res.country containing all the available
    countries.
5.  `default_country`: A res.country record representing the default
    country.
6.  `no_country_placeholder`: A placeholder text for the phone number
    input field.
