To extend this template you need to inherit ``country_dropdown`` template and
add your personal code.

The template have three input text:

#. ``no_country_field``: Field without code country.
#. ``country_code_field``: Field with only country code (read only)
#. ``complete_field``: Field with the previous two joined (hidden)

The name of the complete field is customizable when user insert the snippet
into a form element with the website editor.

Development
~~~~~~~~~~~

You can call the reusable Qweb template called
``website_snippet_country_dropdown.country_dropdown`` in your views to add a
sensible country-combined field, ideal for *VATs*.

The default country will be the first match among:

#. Extract it from the ``default_country`` variable.
#. Extract it from the first 2 letters of the ``default_value`` variable.
#. The current user's country.
#. The current website's company's country.
#. The first country in the list.

All variables you can use to modify its behavior:

* ``complete_field`` to give it a name. Usually it will match the field name.
* ``default_value`` for the ``complete_field``.
* ``countries`` as a ``res.country`` ORM recordset.
* ``default_country`` as a ``res.country`` record.
* ``no_country_placeholder``.

You can view an example in ``website_sale_checkout_country_vat`` in
OCA/e-commerce.
