Register for free website events - Sale extension
=================================================

Extension for module *website_event_register_free* that allows to combine
both kind of registrations: free and paid.

Installation
============

This module will be auto-installed when *website_event_register_free* and
*website_event_sale* are both installed.

Usage
=====

You have two options for events:

* Don't put any type of ticket, so the event will be considered as free, and
  the registration screen of *website_event_register_free* module will appear.
  *Warning:* This doesn't work for now due to a bug in Odoo that doesn't allow
  to store max seats available.
* Define ticket types, but let one or some of the tickets with price 0. When
  you go to normal registration screen, the tickets with price will be added
  to shopping cart, and the priceless tickets will be automatically registered.
  If there are no free tickets selected, then normal checkout screen will
  appeared.

Known issues / Roadmap
======================

* Hide on checkout page the fields that are not needed for free events.
* Move to OCA/event when migrating to v9.

Credits
=======

Contributors
------------

* Pedro M. Baeza <pedro.baeza@tecnativa.com>
* Jairo Llopis <jairo.llopis@tecnativa.com>

Icon
----

* Courtesy of https://creativecommons.org
* Original event module
* Original sale module

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
