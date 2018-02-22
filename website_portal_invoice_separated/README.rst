.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

============================================
Invoices Separated By Type In Website Portal
============================================

This module extends the functionality of the sale and purchase website portals
to support having separate controllers for incoming and outgoing invoices and
allow you to hide unrequired stuff for your portal users.

Installation
============

.. TODO Remove these instructions on v10

To install this module, you need to:

#. Uninstall ``website_portal``.
#. Do not install it as long as you have installed ``website_portal_v10``.

Configuration
=============

To configure this module, you need to:

#. Go to any partner's form.
#. Enable portal access for it.
#. If its company is marked as *customer*, it will only see customer
   (a.k.a. *sale*) part of the portal.
#. If its company is marked as a *supplier*, it will only see supplier
   (a.k.a. *purchase*) part of the portal.

Usage
=====

To use this module, you need to:

#. Go to the sales/purchases order/quotation/invoice you want your
   customer/supplier to see in its portal.
#. Set the partner or its company as follower of the document.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/9.0

Known issues / Roadmap
======================

* This module will have to depend on ``website_portal_sale`` instead of
  ``website_portal_sale_v10`` when migrating to v10.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/website/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Jairo Llopis <jairo.llopis@tecnativa.com>

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
