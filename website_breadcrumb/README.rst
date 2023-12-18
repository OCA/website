.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

===================
Website Breadcrumbs
===================

This module allows you to have breadcrumbs in any page of your website.
But if an URL is not present in a menu (as indicated in the Configuration section), no breadcrumbs will display.

Configuration
=============

To configure the shown breadcrumbs, you need to:

* Go to *Website Admin > Configuration* and click on "Configure website menus".
* Edit any menu there.

Keep in mind that:

* This module will try to match **exactly** the URL in the menu item with the
  one you are browsing.
* If it finds no match, breadcrumbs will not be shown.
* If it finds several matches, only the first one will be used.
* Using more than 1 submenu for the website top menu will probably make it
  unusable. In case you need that granularity, you will have to create a
  separate top menu for managing your breadcrumbs.
* Breadcrumbs use the menu name, **not the page name**, except for the top menu
  item, which will appear as *Home* and point to ``/`` unless you specify an
  URL for it.

Usage
=====

To use this module, you need to:

* Log in.
* Go to your homepage.
* Go to *Customize* menu.
* Enable *Breadcrumbs* (it is enabled by default).

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/9.0


Theming
=======

* If you want to use this module in a theme but you do not like where it is
  rendered, you can simply disable it in the top menu and add in you own
  layout a ``<t t-call="website_breadcrumb.breadcrumb"/>`` element.

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

* Jairo Llopis: Icon.

Contributors
------------

* Jairo Llopis <yajo.sk8@gmail.com>

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
