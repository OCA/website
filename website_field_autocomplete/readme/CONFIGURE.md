There is no backend configuration screen for this module. Configuration is
defined on the website input that should provide autocomplete suggestions.

Before using it, make sure that:

1. The `website` module is installed.
2. The model and fields queried by the autocomplete can be read by the
   website's public user.
3. The website form processes the submitted field configured with
   `data-field`, when one is used.

The endpoint runs searches with the website's public user. Do not expose
sensitive models or fields, and use `data-domain` to restrict the records that
can be suggested when the model contains data that should not be offered to
website visitors.

For a relational value, use `data-value-field="id"` and set `data-field` to
the name of the hidden form field that must receive the selected record ID.
The hidden field is created automatically when it is missing from the form.
