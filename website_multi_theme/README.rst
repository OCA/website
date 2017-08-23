.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

===================
Website Multi Theme
===================

Allow the website admin to set a different theme for each website.

Installation
============

To make this module work, you need to either:

* Install any of the officially supported themes:

  * theme_bootswatch

* Install any of the unofficially supported themes (at your own risk):

  * theme_anelusia
  * theme_artists
  * theme_avantgarde
  * theme_beauty
  * theme_bewise
  * theme_bistro
  * theme_bookstore
  * theme_clean
  * theme_enark
  * theme_graphene
  * theme_kea
  * theme_loftspace
  * theme_mongolia
  * theme_nano
  * theme_notes
  * theme_odoo_experts
  * theme_orchid
  * theme_treehouse
  * theme_vehicle
  * theme_yes
  * theme_zap

Themes in the above lists will become multiwebsite when installed along this
module. **If they get installed after ``website_multi_theme``, update this
module manually**, or it will not be notified of such change.

Configuration
=============

To configure this module, you need to:

#. Go to *Website Admin > Configuration > Settings* and choose or create
    a *Website*.
#. Press *Advanced > Multiwebsite theme > Reload*.
#. In *Advanced > Multiwebsite theme*, pick one of the available themes.

Once you save, any website that has no *Multiwebsite theme* selected will have,
the default plain Bootstrap theme, and those that do have one will get it.

Of course, your Odoo instance must be reachable by all of the provided host
names, or nobody will ever see the effect. But that is most likely configured
through your DNS provider and/or proxy, so it is not a matter of this addon.

If you want to test this behavior, think that ``localhost`` and ``127.0.0.1``
are different host names.

Usage
=====

To use this module, you need to:

#. Follow the configuration steps.
#. Enter any of the websites you modified.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/10.0

Development FAQ
===============

How to develop a multiwebsite-ready theme?
------------------------------------------

Check ``demo/themes.xml``. It includes a demo theme that will serve as a
template for you. This demo theme turns primary buttons green, so you can test
if it is applied or not easily.

How to convert a single-website theme in a multi-website one?
-------------------------------------------------------------

Check ``data/themes_bootswatch.xml``. You must do that. You can consider adding
the support directly in this addon, given it will just do nothing if the
single-website theme addon is not installed (it acts as a soft dependency).

How to get multiwebsite-specific views updated?
-----------------------------------------------

This addon is conservative by default, meaning that in production databases
views will not be updated if they already were created (except for the ones
copied from ``templates/patterns.xml``).

To force your website getting updated views for all views from a base theme
that has changed, you should disable the website multi theme (to make the
engine remove all views) and then re-enable it again (to recreate them from
scratch).

This does not happen in demo or development instances, where views arch is
always updated.

Known issues / Roadmap
======================

* Private themes support is not guaranteed.
* There is no UI to remove websites. Do it through an odoo shell.
* Theme picker should include some kind of thumbnail if possible.
* If you install any of the supported themes after installing this addon, you
  will have to press *Reload* in the website config wizard to make it notice
  the change.
* If you install any unsupported theme along with this addon, it would possibly
  become the base for all those supported, which can easily lead to weird
  situations and errors.
* This addon will not work if your Odoo is not patched. Make sure it is updated
  before installing. It must include these commits:

  - https://github.com/odoo/odoo/commit/15bf41270d3abb607e7b623b59355594cad170cf
  - https://github.com/odoo/odoo/commit/7c6714d7fee4125f037ef194f9cff5235a6c5320
  - https://github.com/odoo/odoo/commit/48fe0a595308722a26afd5361432f24c610b4ba0

Credits
=======

Contributors
------------

* Rafael Blasco <rafael.blasco@tecnativa.com>
* Antonio Espinosa <antonio.espinosa@tecnativa.com>
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
