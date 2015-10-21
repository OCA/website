.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

Collapsible product categories in website shop
==============================================

This module changes categories list to allow to collapse them.

This is a backport from Odoo v9 feature of this branch:
https://github.com/odoo-dev/odoo/tree/master-collapse-public-category-gan

Installation
============

Install the module the regular way.

Configuration
=============

On website shop page having edit permission, click on Customize, and select
"Collapse product categories" to use this feature.

Usage
=====

First level categories are shown, but collapsed by default, hidding their
children categories. Click on the down arrow to uncollapse them, and click
on a category to select it. The selected category path will remain unfolded
when loading category page.

Known issues / Roadmap
======================

This module won't be needed on v9, because it is already part of the core
functionality, because of this PR: https://github.com/odoo/odoo/pull/4830.

Credits
=======

Contributors
------------

* OpenERP S.A.
* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>

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
