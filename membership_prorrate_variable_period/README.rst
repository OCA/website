=================================================
Prorrate the membership fee with variable periods
=================================================

Helper module for making the prorrate correctly when you are dealing with
variable periods in your memberships, which functionality is provided by
the module *membership_variable_period*.


Installation
============

This module is auto-installed if you have *membership_variable_period* and
*membership_prorrate* modules installed.

Usage
=====

For leading with variable periods and prorrate, only weekly, monthly or yearly
periods are allowed. When you create an invoice with a membership product
with variable period, the theoretical period is calculated from the invoice
date (or today if empty) as the natural period of the selected unit that
includes that date. For example, if the invoice is on the 15th of January
and the unit is month, the theoretical period to invoice will be all the month
of January.

Known issues / Roadmap
======================

* Allow to handle periods of months that make the year divisible: 2 months
  (two-monthly), 3 months (quartely), 4 months (four-monthly) or 6 months
  (biannual).
* On weekly memberships, consider the duality sunday/monday start of the week.

Credits
=======

Contributors
------------

* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>

Icon
----

Original clipart from:

* http://pixabay.com/es/en-contacto-con-tarjeta-de-cr%C3%A9dito-97574/
* https://openclipart.org/detail/153745/barre-de-progression

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
