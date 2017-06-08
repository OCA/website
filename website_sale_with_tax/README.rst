.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: AGPLv3 License

Product prices with taxes on e-commerce
=======================================

This addon shows the correct price indepently of the tax configuration
(with or without the "Tax included in price" check).

It takes care of tax configuration: price_include, showing prices
with tax included even "Tax included in price" is check (price_include == True)
or unckecked (price_include == False)

This helps to shop owner because he can set product prices with or without taxes,
but prices are always shown in website shop with taxes


Usage
======
First you need to check permissions in Odoo, activate Technical Features in Settings/USers and set the Financial Manager permissions in Accounting and Finance

Go to Invoicing/Taxes and create one
You have to check tax included to try the usability
Go back to Sales/products and select the product you are going to buy in the website and add the taxes in the product
Then check in the shop cart both options, when you buy a product tax included or tax excluded

Credits
=======

Contributors
------------

* Antonio Espinosa <antonioea@antiun.com>
* Endika Iglesias <endikaig@antiun.com>

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

