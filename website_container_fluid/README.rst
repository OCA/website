.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

Snippet container width type chooser
====================================

This module was written to extend the functionality of the website editor to
support choosing the width type between the available `Bootstrap container
types <http://getbootstrap.com/css/#overview-container>`_:

* **Fixed**, which will have a fixed width that will depend on the user's
  screen width, and usually will have an empty margin at each side.

* **Fluid**, which will always fill 100% of the available width space.

Odoo's default value is usually **Fixed**, and remains the same.

Usage
=====

To use this module, you need to:

* Go to any website page.
* Press *Edit*.
* Press *Insert blocks*.
* Insert any block that uses a container, such as *Text block*.
* Click on an inner element and press *Select container block* (the button to
  select current element's parent) until you get to an HTML element with the
  class `container` or `container-fluid`.
* Select *Customize > Container width type* and choose one from there.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/9.0

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
