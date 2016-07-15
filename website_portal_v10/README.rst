.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

====================================
Website Portal (Backported From v10)
====================================

This module replaces the functionality of ``website_portal`` to support sane
layout and extensibility and to allow you to have a special layout just for
portal pages, to have custom controllers for pages, to have a menu indicating
all sections for the portal features, to inherit everything without problems,
and to prepare for forward compatibility.

.. warning::
    This module depends on ``website_portal``, but it **replaces** it. If you
    install other module based on ``website_portal`` that is not adapted to
    this version, it could work, but there is no guarantee. If you are
    developing a website portal module, we recommend you to do it based on this
    one instead, and get those extra benefits.

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
#. Enjoy the new layout.

.. warning::
    This module is just a base for other modules. When you install those
    others, you will actually see something useful in your account.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/9.0

Known issues / Roadmap
======================

* This module was born because the core implementation of ``website_portal`` in
  Odoo 9.0 is considered to be broken by some people. Odoo 10.0 will fix that,
  but we want it all, and we want it now.
* This module should be getting updates from time to time, given that at
  backporting time, Odoo 10.0 is not yet even in the beta phase.
* To avoid some incompatibilities between ``website_portal`` and
  ``website_portal_v10``, this module depends on ``website_portal`` and tries
  to replace just the bits that are new or different in v10. As such, a plain
  backport without 3-way diffing between this, core v9 and core v10 modules
  is quite hard.
* Any module you base on this will need to be updated to be based on
  ``website_portal`` when you migrate it to Odoo 10.0, because this module is
  only intended to replace that during the 9.0 lifespan.
* If you install ``website_portal_v10`` and then uninstall it, you need to
  reinstall ``website_portal`` to restore some of this module's changes. Then,
  you can safely remove any ``ir.ui.view`` object belonging to
  ``website_portal_v10``.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/website/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and
welcomed feedback.

Credits
=======

**This module is a backport from Odoo SA and as such, it is not included in the
OCA CLA. That means we do not have a copy of the copyright on it like all
other OCA modules.**

Contributors
------------

* `Contributions to original module
  <https://github.com/odoo/odoo/commits/master/addons/website_portal>`_
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
