.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==========================
Locations in website blogs
==========================

This module was written to allow you to attach a location to a blog entry.

Users will then be able to navigate to ``/blogmap/<blogid>`` and see a map where blog entries can be selected by location.

Usage
=====

To use this module, you need to:

#. go to Knowledge/Blog posts
#. select some blog post
#. enter a latitude and longitude
#. click the `Show in map` link and be happy to see your blog post there
#. link to ``/blogmap/<blogid>`` in some menu or page
#. alternatively, enable the right column for your blog in the frontend, and enable the option `Show in map`. This generates a link to the map

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
    :alt: Try me on Runbot
    :target: https://runbot.odoo-community.org/runbot/186/8.0

Known issues / Roadmap
======================

* adding the latitude/longitude fields on the frontend would be a lot more user friendly
* use a map widget to select the location
* add a snippet to show the map
* custom markers would be nice
* some of the code already tries to be more generic. In the end, we should have some base module that shows maps for arbitrary records, and have this one depend on it
* in the end, there probably should be an openlayers base module where users can configure which mapping engine to use etc.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/website/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Holger Brunn <hbrunn@therp.nl>

Do not contact contributors directly about help with questions or problems concerning this addon, but use the `community mailing list <mailto:community@mail.odoo.com>`_ or the `appropriate specialized mailinglist <https://odoo-community.org/groups>`_ for help, and the bug tracker linked in `Bug Tracker`_ above for technical issues.

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
