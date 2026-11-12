Add an input field with the `js_website_autocomplete` class to a website
template or form. `data-model` is the only required data attribute:

```html
<input
    type="text"
    name="partner_name"
    class="form-control js_website_autocomplete"
    data-model="res.partner"
    data-query-field="name"
    data-display-field="name"
    data-value-field="id"
    data-field="partner_id"
    data-limit="10"
    data-domain='[["is_company", "=", true]]'
>
```

When the visitor types, the module searches `data-query-field` with an
`ilike` condition and displays the matching values. Selecting a suggestion
puts its label in the visible input and, when `data-field` is set, its value
in a hidden input with that name. Suggestions can also be selected with the
arrow keys and `Enter`; `Escape` closes the list.

Available attributes:

| Attribute | Required | Default | Description |
| --- | --- | --- | --- |
| `data-model` | Yes | — | Technical name of the model to search. |
| `data-field` | No | — | Name of the hidden form field that receives the selected value. |
| `data-query-field` | No | `name` | Field searched with the visitor's text using `ilike`. |
| `data-display-field` | No | `data-query-field` | Field whose value is shown in the suggestions and visible input. |
| `data-value-field` | No | `data-display-field` | Field whose value is written to `data-field`; use `id` to submit a record ID. |
| `data-limit` | No | `10` | Maximum number of suggestions. The server clamps it between 1 and 100. |
| `data-domain` | No | `[]` | Additional domain encoded as a JSON array, appended to the text search domain. |

For example, a many2one-like website form can show a partner name while
submitting its ID in `partner_id`:

```html
<input
    type="text"
    class="form-control js_website_autocomplete"
    data-model="res.partner"
    data-query-field="name"
    data-display-field="name"
    data-value-field="id"
    data-field="partner_id"
>
```

The autocomplete request is sent to
`/website/field_autocomplete/<model>` as a public website JSON-RPC request.