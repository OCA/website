.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl
   :alt: License: LGPL-3

=========================
Website Snippet - Barcode
=========================

This module provides a barcode snippet to website, allowing the generation and
display of various types of barcodes.

Usage
=====

To use this module, you need to:

#. Edit a web page
#. Find Barcode in the Blocks sidebar, in the "Inner Content" section.
#. Drag the Barcode snippet to the desired location
#. Adjust options as needed
#. Save the page

Barcode Options
---------------

**Barcode Type**

* All barcode types available in the report module are available in this
  snippet.
* Certain barcode types are not compatible with certain values, but this will
  be apparent during selection.
* *Default: QR*

**Barcode Value**

* This is the value represented by the barcode. Accepts the current page URI or
  a custom string value.
* *Default: URI of current page*

**Aspect Ratio**

* This setting adjusts the width-to-height ratio of the barcode image.
* *Default: 1:1 (square)*

**Human Readable**

* This setting controls the display of barcode values in human-readable format.
* **None**: Human-readable value is not displayed.
* **Text**: Display the human-readable value as a caption below the
  image.
* **Image**: *Not supported by all barcode types.* Include the human-readable
  value in the generated image.
* *Default: None*

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/10.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/website/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Brent Hughes <brent.hughes@laslabs.com>

Do not contact contributors directly about support or help with technical issues.

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
