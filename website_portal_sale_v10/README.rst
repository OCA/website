.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

==============================================
Website Portal for Sales (Backported From v10)
==============================================

This module replaces the functionality of ``website_portal_sale`` to support
changes introduced in ``website_portal_v10``. See README of
``website_portal_v10`` about rationale for this module and some useful
warnings.

.. warning::
    This module is intended to **replace** ``website_portal_sale``, and is
    **not compatible** with it. If you install both modules, expect bad things
    to happen. If you are developing a new module based on
    ``website_portal_sale``, we recommend you to do it based on this one
    instead, and get those extra benefits.

.. warning::
    If you want to patch any bug or improvement on this module, remember **this
    is a backport**. We should not have any custom fixes or improvements here.
    Rather than that, try to get your patch merged in Odoo v10 and update this
    backport when done.

Installation
============

To install this module, you need to:

#. Uninstall ``website_portal``, if it was installed, and don't install it
   again as long as this module is installed.

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
  ``website_portal_sale`` when you migrate it to Odoo 10.0, because this module is
  only intended to replace that during the 9.0 lifespan.

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
