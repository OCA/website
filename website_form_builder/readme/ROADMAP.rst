* These type of fields will not appear, they are forbidden since they make no
  sense in this module's context, or a correct implementation would be adding
  not much value while adding lots of complexity:

  * ``id``
  * ``create_uid``
  * ``create_date``
  * ``write_uid``
  * ``write_date``
  * ``__last_update``
  * Any ``one2many`` fields
  * Any ``reference`` fields
  * Any ``serialized`` fields
  * Any read-only fields

* You should include https://github.com/odoo/odoo/pull/21628 in your
  installation to get a better UX when a user has already sent a form and
  cannot resend it.

* To edit any ``<label>`` text, you need to click twice. Review the problem
  once https://bugzilla.mozilla.org/show_bug.cgi?id=853519 gets fixed.

* You cannot edit base fields blacklisted status manually because
  `Odoo forbids that for security
  <https://github.com/OCA/website/pull/402#issuecomment-356930433>`_.

* ``website_form`` works in unexpected and undocumented ways. If you plan to
  add support in your addon, `this is a good place to start reading
  <https://github.com/OCA/website/pull/402#discussion_r157441770>`_.

* If you add a custom file upload field to a form that creates records in
  models that have no ``mail.thread`` inheritance, your users will be unable
  to send the form.
