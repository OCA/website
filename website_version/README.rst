.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

===============
Website Version
===============

This module extends the functionality of the website by adding versionning
of pages and A/B testing.

Usage
=====

When viewing a website page that you can modify, you will see a "Version"
menu on the top bar that will let you create different versions of a page
without publishing it.

When saving an edited page, you will have to select between publishing your
changes directly or saving them into a new version that you can publish at
a later date.

Known issues / Roadmap
======================

* Making a new version from another only copies pages that were modified
  in the source version.
  As a side-effect making a new version from master creates a version containing
  a single-page.
* A/B testing only works with Google Analytics right now.
  Work is planned on Mautic and Piwik A/B testing support.

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

* Odoo S.A. <https://www.odoo.com/>
* Clouder SASU <https://goclouder.net/>
* Nicolas Petit (Clouder) <https://github.com/nicolas-petit/>

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
