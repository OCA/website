.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl
   :alt: License: LGPL-3

====================
Website Form Builder
====================

This module provides websites the feature of adding custom forms in any page.

Installation
============

Install some other addon that provides ``website_form`` support to
benefit from this one's features. Hints:

* ``website_crm``
* ``website_form_project``
* ``website_hr_recruitment``
* ``website_sale``

Configuration
=============

To configure this module, you need to:

#. Have *Administration / Settings* privileges.
#. Go to *Settings > Activate developer mode*.
#. Go to *Settings > Technical > Database Structure > Models*.
#. Search for the model you want to manage website form access for.
#. When you find it, it will have a *Website Forms* section where you can:

   * Allow the model to get forms, by checking *Allowed to use in forms*.
   * Give the model forms a better name in *Label for form action*.
   * Choose the field where to store custom fields data in *Field for custom
     form data*. If you leave this one empty and the model is a mail thread,
     a new message will be appended with that custom data.

#. In the *Fields* tab, there's a new column called *Blacklisted in web forms*.
   It's a security feature that forbids form submitters to write to those
   fields. When you create a new website form, all its model fields are
   automatically whitelisted for the sake of improving the UX. If you want to
   have higher control, come back here after creating the form and blacklist
   any fields you want, although that will only work for custom fields.

Usage
=====

To use this module, you need to:

#. Go to any of your website pages.
#. Edit it.
#. Drag and drop the *Form* snippet into the page.
#. Use the snippet overlay to add, edit and remove fields.
#. If you want to set a hidden field, make sure you set a valid default value
   on it, or users may get hidden errors and they might even be unable to send
   the form!

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/10.0

Known issues / Roadmap
======================

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

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/website/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* https://openclipart.org/detail/281632/form
* https://openclipart.org/detail/224192/simple-grey-small-pencil-icon-white-background

Contributors
------------

* `Tecnativa <https://www.tecnativa.com>`_:
  * Jairo Llopis <jairo.llopis@tecnativa.com>

Do not contact contributors directly about support or help with technical issues.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
