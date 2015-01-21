Backend views for website
=========================

This module allows to embed old style (backend) views into the website frontend. This way, complex forms don't need to be redeveloped but still there's no break in user experience. Caveat is that this does not work for anonymous users.

This is specifically convenient if you need to use on_change functions, user input dependent domains or got used to be able to create linked objects inline.

Usage
=====

Install this module with demo data enabled and visit `/website_backend_views/demo`. Then read `view/demo.xml`.

Known issues / Roadmap
======================

* more testing needed
* not all css styles from the backend apply (should be just a matter of having the right html structure/classes attached to the container)
* maybe we can do something for anonymous users?
* view switching?

Credits
=======

Contributors
------------

* Holger Brunn <hbrunn@therp.nl>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
    :alt: Odoo Community Association
    :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
