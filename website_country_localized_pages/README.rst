.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Country specific web pages
==========================

Use this module to create localized web pages according to visitor's country.


Installation
============

To install this module, you need ipwhois
https://pypi.python.org/pypi/ipwhois


Configuration
=============

Example
-------

Through CMS (frontend website) interface, create for instance a new 'US features' page for Unites States, without adding it to the menu, and fill it with US specific content.

Then, go to
Settings -> Technical -> User interface -> Views
search for standard 'features' page, go to 'country specific views' tab, add one line selecting 'US' country and 'US features' page.

Visitors from Unites States will see the 'US features' page instead of the standard one.

Known issues / Roadmap
======================

* Ddding a way to let the user opt-out of the localized pages, or switch to another localization

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/website/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/website/issues/new?body=module:%20website_country_localized_pages%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Lorenzo Battistini <lorenzo.battistini@agilebg.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
