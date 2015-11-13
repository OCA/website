.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Snippet Background Style
========================

This module was written to extend the functionality of the website editor to
support choosing more options when setting a background image to any element.

Available choices are under these categories:

* `Position
  <https://developer.mozilla.org/en-US/docs/Web/CSS/background-position>`_.
* `Repeat
  <https://developer.mozilla.org/en-US/docs/Web/CSS/background-repeat>`_.
* `Size
  <https://developer.mozilla.org/en-US/docs/Web/CSS/background-size>`_.

Usage
=====

To use this module, you need to:

* Go to any website page.
* Press *Edit*.
* Press *Insert blocks*.
* Insert any block that can have a background image, such as *Text block*.
* Set a background image for it.
* Use the new option *Customize > Background style* and select any option you
  like.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/8.0

Known issues / Roadmap
======================

* Right now you can only select one style for every snippet. To fix that we
  would need to base this module in *website_less*, whose source code is not
  available in OCA. In version 9.0 this will be fixed, but in version 8.0 you
  will have to use only one option or set the correct CSS classes using the
  HTML editor.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/website/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and
welcomed feedback `here
<https://github.com/OCA/website/issues/new?body=module:%20website_img_bg_style%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Jairo Llopis <j.llopis@grupoesoc.es>

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
