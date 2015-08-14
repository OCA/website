========================
Website Portal for Sales
========================

Backport (with adjustments) of the ``website_portal_sale`` module of Odoo 9.

This module add the user's sales documents in the frontend portal.
Customers will be able to see the list and state of their quotations, sales
and invoices.

Known Issues / Roadmap
======================

* In v9, the field ``validity_date`` of the sale order has been moved from the
  ``website_quote`` module to the base ``sale`` module, therefore the module
  references it without problem as the ``sale`` module is a dependency of this
  one.
  For version 8 the validity_date on the portal has been removed completely at
  the moment. Instead, we should make a conditional template that shows the field
  if the ``website_quote`` module is installed.
* Tests

Credits
=======

Contributors
------------

* Odoo SA <https://www.odoo.com>
* Leonardo Donelli @ MONK Software <donelli@webmonks.it>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
