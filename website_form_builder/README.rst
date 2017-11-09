.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl
   :alt: License: LGPL-3

====================
Website Form Builder
====================

This module provides websites the feature of adding custom forms in any page.

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
   any fields you want.

Usage
=====

To use this module, you need to:

#. Go to any of your website pages.
#. Edit it.
#. Drag and drop the *Form* snippet into the page.
#. Use the snippet overlay to add, edit and remove fields.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/10.0

Known issues / Roadmap
======================

* These type of fields will not appear, they are forbidden since they make no
  sense in this module's context, or a correct implementation would be adding
  not much value while adding lots of complexity:

  * ``id``
  * ``one2many``
  * ``reference``
  * ``serialized``

* You should include https://github.com/odoo/odoo/pull/21628 in your
  installation to get a better UX when a user has already sent a form and
  cannot resend it.

* To edit any ``<label>`` text, you need to click twice. Review the problem
  once https://bugzilla.mozilla.org/show_bug.cgi?id=853519 gets fixed.

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
