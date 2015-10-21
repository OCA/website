.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

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

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/website/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and
welcomed feedback `here
<https://github.com/OCA/website/issues/new?body=module:%20website_container_fluid%0Aversion:%208.0.1.0.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


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
