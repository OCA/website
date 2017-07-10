.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

====================
Set Snippet's Anchor
====================

This module extends the functionality of the website editor to support setting
an anchor to any section of your web page and allow you to link to them very
easily.

Anchors are just the HTML ``id`` attribute, which is commonly used to add it
to any URL and get directly to the element with that anchor, in the form of
https://www.tecnativa.com/#anchor-name.

Usage
=====

Valid character ranges for anchors are: ``[A-Z][a-z][0-9]_-``

To add an anchor to any element, you need to:

* Edit any web page.
* Go to *Add blocks > Structure*.
* Insert any block in your page.
* Click on the snippet's option *Customize > Choose anchor*.
* Set an anchor. If it is already used or has an invalid format, you will be
  asked to use another.

To link to any page's anchor, you need to:

* Edit any web page.
* Select some text.
* Press *Link* in the editor toolbar.
* Choose a page in the opened dialog.
* Set an anchor there too (without ``#`` symbol).
* Press *Save*.

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

* Rafael Blasco <rafael.blasco@tecnativa.com>
* Jairo Llopis <jairo.llopis@tecnativa.com>

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
