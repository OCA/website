.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

==============================================
Website Portal for Sales (Backported From v10)
==============================================

This module replaces some functionality of ``website_portal_sale`` to support
changes introduced in ``website_portal_v10``. See README of
``website_portal_v10`` about rationale for this module and some useful
warnings.

Installation
============

This will be automatically installed when both ``website_portal_sale`` and
``website_portal_v10`` are found in your system.

Usage
=====

To use this module, you need to:

#. Go to `your website </>`_.
#. Go to `your account </my/home>`_.
#. There you will find the links for your sale documents, in independent
   controllers.
#. Enjoy the new layout.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/9.0

Known issues / Roadmap
======================

* This module should be getting updates from time to time, given that at
  backporting time, Odoo 10.0 is not yet even in the beta phase.
* Any module you base on this will need to be updated to be based on
  ``website_portal_sale`` when you migrate it to Odoo 10.0, because this module
  is only intended to replace that during the 9.0 lifespan.
* Backport had to be modified to avoid conflicts betweeen current and v10
  versions of modules, so backport updates would be a bit harder than expected.

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

* `Contributions to original module
  <https://github.com/odoo/odoo/commits/master/addons/website_portal_sale>`_
  belong to their owners.
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
