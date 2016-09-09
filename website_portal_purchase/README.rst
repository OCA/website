.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3

============================
Website Portal for Purchases
============================

This module adds the partner's purchase documents in the frontend portal.
Suppliers will be able to see the list and state of their request for
quotations, purchase orders and supplier invoices.

.. warning::
    "Purchases" term here refers to your company's POV about purchases. That
    means this module actually creates a portal *for your suppliers*.

Usage
=====

To use this module, you need to:

1. Assign auth user group to the user.
2. If you install 'portal_sale' you can invite user to access it.
3. User can access to his request quotations, orders and supplier invoices
   from his account in user account link.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/9.0


Known issues / Roadmap
======================

* Tests.
* When migrating to v10, we will have to base this module on ``website_portal``
  directly.
* If you want to display invoices, you will have to install
  ``website_portal_sale_v10``, which displays both customer and supplier
  invoices merged in the same place.

  * If you do not want both kinds of invoices merged in the same controller,
    install ``website_portal_invoice_separated``.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/website/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and
welcomed feedback.

Credits
=======

Contributors
------------

* Rafael Blasco <rafabn@antiun.com>
* Carlos Dauden <carlos@incaser.es>
* Sergio Teruel <sergio@incaser.es>
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
