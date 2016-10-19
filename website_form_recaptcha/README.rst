.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Website Form - ReCaptcha
========================

Adds a ReCaptcha field widget for website forms


Configuration
=============

* Obtain ReCaptcha key from `Google <http://www.google.com/recaptcha/admin>`_
* Add site key to `recaptcha.key.site` system parameter
* Add secret key to `recaptcha.key.secret` system parameter

Usage
=====

To use this module, you need to:

* Already have a form-enabled model
* Set `website_form_recaptcha` to `True` on that model (similar to enabling forms)
* Add an element with the `o_website_form_recaptcha` class anywhere in the form

Look at `website_crm_recaptcha` module for example implementation


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/10.0


Known Issues / Road Map
=======================

* Add domain validation


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

* Dave Lasley <dave@laslabs.com>

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
