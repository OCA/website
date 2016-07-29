.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

==================================================
Payment: Website Integration (Backported From v10)
==================================================

This module updates the functionality of ``website_payment`` to support
changes introduced in ``website_portal_v10``. See README of
``website_portal_v10`` about rationale for this module and some useful
warnings.

Usage
=====

To use this module, you need to:

#. Go to `your website </>`_.
#. Go to `your account </my/home>`_.
#. Enable payment method editing from *Customize > Portal Layout >
   Payment Methods*.
#. Go to `Manage your payment methods </my/payment_method>`_.
#. Enjoy the new layout.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/9.0

Known issues / Roadmap
======================

* Any module you base on this will need to be updated to be based on
  ``website_payment`` when you migrate it to Odoo 10.0, because this module is
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
  <https://github.com/odoo/odoo/commits/master/addons/website_payment>`_
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
