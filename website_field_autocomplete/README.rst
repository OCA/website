.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Website Field - AutoComplete
============================

Adds an AutoComplete field for use in Odoo Website.

This module is somewhat difficult to use on its own in an effort to not require
any dependencies other than website.

Usage
=====

To use this module, you need to add an input field with the
``js_website_autocomplete`` class, such as in the below format:

.. code:: xml

    <input type="text"
           class="js_website_autocomplete"
           data-query-field="name"
           data-display-field="name"
           data-value-field="id"
           data-limit="10"
           data-domain='[["website_published", "=", true]]'
           data-model="product.template"
           />

Following is a breakdown of the available attributes & their defaults:

+--------------------+---------------------------------------------+---------------+----------+
|  Attribute         |  Description                                |  Default      | Required |
+====================+=============================================+===============+==========+
| data-model         | Model name to query                         |               | True     |
+--------------------+---------------------------------------------+---------------+----------+
| data-query-field   | Field to query when searching               | name          | False    |
+--------------------+---------------------------------------------+---------------+----------+
| data-display-field | Field to display                            | query-field   | False    |
+--------------------+---------------------------------------------+---------------+----------+
| data-value-field   | Field to use as form value                  | display-field | False    |
+--------------------+---------------------------------------------+---------------+----------+
| data-limit         | Limit results to this many                  | 10            | False    |
+--------------------+---------------------------------------------+---------------+----------+
| data-domain        | Additional domain for query                 | []            | False    |
+--------------------+---------------------------------------------+---------------+----------+


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/10.0


Known Issues / Road Map
=======================

* Replace jQuery UI Autocomplete w/ HTML5 Datalist when `ready for production <http://caniuse.com/#feat=datalist>`_.


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
