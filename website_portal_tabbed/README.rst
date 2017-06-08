.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Tabs in Website Portal
======================

This module extends the functionality of the website portal sales and purchases modules to support separating those 2 areas in a tabbed interface.

Installation
============

To install this module, you need to:

#. Install `website_portal_purchase
   <https://www.odoo.com/apps/modules/9.0/website_product_supplier/>`_.

Usage
=====

To use this module, you need to:

#. Log in as a user that is both a customer and a supplier.
#. In the main website, go to `My Account </my/home>`_.
#. Use the tabs for your documents separated by role.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/9.0

Known issues / Roadmap
======================

* This module should not depend on ``website_portal_sale`` and
  ``website_portal_purchase``, but just check if those are installed and then
  modify views according to that, to allow to have a tabbed website portal for
  other purposes, but right now it's its only purpose, and achieving that is
  not specially easy.
* It should do the same with ``website_project_issue``.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/website/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

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
