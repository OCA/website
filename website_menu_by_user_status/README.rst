.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Website Menu By User Status
===========================

The module manages display website menu entries, depending if the user is
logged or not.
The selection of the display status can be chosen logged and/or not.
Extends features and view of website.menu model.
But for modules that install new routes like _your_wesite_/shop or _your_wesite_/event
the redirection will not work in such cases.

Installation
============

To install this module, just click to install butto

Configuration
=============

#. you must activate the developer mode

Usage
=====

To use this module, you need to edit website menu pages list view that can be found at :
Website Admin > Configuration > Settings > Configure website menus

#. remove default filter to edit website menu line

The module inherit from website.menu to add 2 booleans fields, user_logged
and user_not_logged.
On top of that, website.layout template is extended to include a condition
that drive if the menu is built or not.
It has been choose to not only hide the menu to avoid to easily get around
by editing the html DOM.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/website/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.


Contributors
------------
* Bruno Joliveau <bruno.joliveau@savoirfairelinux.com>
* Jordi Riera <jordi.riera@savoirfairelinux.com>
* Meyomesse Gilles <meyomesse.gilles@gmail.com>

More information
----------------
Module developed and tested with Odoo version 10.0
For questions, please contact our support services
<support@savoirfairelinux.com>

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