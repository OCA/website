.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Discounts in product supplier info - For sales
==============================================

Using the modules *product_supplierinfo_for_customer* and
*product_supplierinfo_discount* that enables respectively to use the
supplier info also for customers and to set a discount in it, this module
allows to propagate that discount in sales orders.

Installation
============

This module requires *purchase_discount* and *product_supplierinfo_discount*
modules, that are available in repository OCA/purchase-workflow, and
*product_supplierinfo_for_customer*, that is available on this repository.

Configuration
=============

To see prices and discounts on supplier info view, you have to enable the
option "Manage pricelist per supplier" inside *Configuration > Purchases*

Usage
=====

Go to Purchase > Products, open one product, and edit or add a record on the
*Customers* section of the *Sales* tab. You will see in the prices section
in the down part a new column called *Discount (%)*. You can enter here
the desired discount for that quantity.

When you make a sale order for that customer and that product, the discount
will be put automatically.

Known issues / Roadmap
======================

* The discount is always applied, independently if you have based
  your pricelist on other value than "Supplier Prices on the product form".

Credits
=======

Contributors
------------

* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>

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
