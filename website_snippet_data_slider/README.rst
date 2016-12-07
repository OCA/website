.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

=============================
Website Snippet - Data Slider
=============================

Adds a SlickJS slider building block to website allowing for the query and
display of abstract datasets.

Example uses for this module:

* Products slider using the ``product.product`` model
* Affiliates slider using the ``res.partner`` model

.. image:: static/description/screenshot.png?raw=true
   :alt: Data Sliders

Usage
=====

To use this module, you need to:

* Install `website_snippet_data_slider` module
* Drop `Data Slider` building block anywhere on your site
* Edit the configuration options to your liking
* Save
* Profit!


Note that the snippet defaults to the `product.template` model, as most common
usage for this widget is likely a product carousel.

Odoo snippet settings Javascript somewhat of got in the way when it came to allowing
easy choice of the data, aside from the simple options that were provided in the UI.

In order to further customize your snippet, go into HTML view and edit the
`data-options` attribute of the `section` element that serves as the snippet root.

Following are the setings that do not have configuration in the UI:

* `data_model` - Model name
* `data_domain` - Search domain for data
* `data_limit` - Limit query to this many results
* `data_image_field` - Field name to use for image
* `data_name_field` - Field to use for display name
* `data_title` - Text to use as main snippet header
* `data_title_tag` - HTML element type to use for title element (such as `h1`)
* `data_title_class` - Class to use for the title element
* `data_uri_field` - Field to use for the link
* `data_container_width` - Width of the outer container, default 90%
* `prevArrow` & `nextArrow` - HTML or jQuery selector of slider arrows

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/10.0

Known Issues / Road Map
======================

* Provide UI for data settings
* Provide responsive settings & config
* Consolidate the data options a bit?
* Find a way to use slug, instead of URI Prefix
* Touch up the stylesheets
* Add a real thumbnail, instead of icon

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

* Dave Lasley <dave@laslabs.com>

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
