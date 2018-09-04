.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

===================
Website Multi Theme
===================

Allow the website admin to set a different theme for each website.

The *theme* might be not just a theme-module, but any set of themes and even
particular views from any module (e.g. view ``website.custom_footer`` from
``website`` module). It also means, that *theme* is not just a styling, but
a content as well.

It adds controls to make managing multiple websites easier:

* Drop-down list to switch to a different website.
* Change the related website of pages in the page properties dialog with checkboxes.
* Adds the field `website_ids` to the `website.page` tree.

How it works
============

Core idea is as following

* Find views created by *theme-module* and mark them as *multi-views* (``website.theme.asset``) additionally to one specified manually via XML (see `demo/themes.xml <demo/themes.xml>`_ as an example). The method `_convert_assets <models/website_theme.py>`_ is responsible for it.

* Set ``active`` to ``False`` for *multi-views*. See method `_find_and_deactivate_views <models/website_theme.py>`_.

* Apply *Multi-theme* (record in new model ``website.theme``) to the specific
  website. See method `_multi_theme_activate <models/website.py>`_

  * Make some magic with technical views ``website.assets_frontend`` and ``website.layout``.

    * Duplicate *patterns* from `templates/patterns.xml <templates/patterns.xml>`_
    * In ``layout_pattern`` replace ``{theme_view}`` placeholder to a duplicate
      of ``assets_pattern``
    * Corresponding duplicated *pattern* will be used as a new value for
      ``inherit_id`` field in duplicated *multi-views* that originally extend
      ``web.assets_frontend``, ``website.assets_frontend`` or
      ``website.layout``.

  * Duplicate *multi-views* of the *multi-theme* and its *dependencies* (other
    *multi-themes*). In duplicates, the field ``inherit_id`` is changed to other
    duplicated views or duplicated *patterns* when possible

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
#. Via Edit button (``fa-external-link``) add *Default Theme* to *Sub-themes* of
   the selected theme to make multi-footer work.

Once you save, any website that has no *Multiwebsite theme* selected will have,
the default plain Bootstrap theme, and those that do have one will get it.

Of course, your Odoo instance must be reachable by all of the provided host
names, or nobody will ever see the effect. But that is most likely configured
through your DNS provider and/or proxy, so it is not a matter of this addon.

If you want to test this behavior, think that ``localhost`` and ``0.0.0.0``
are different host names.

Usage
=====

To use this module, you need to:

#. Follow the configuration steps.
#. Enter any of the websites you modified.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/11.0

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

How to test on runbot?
----------------------

* Open ``[[ Website ]] >> Configuration >> Settings``
* Switch *Website* field from ``Website localhost`` to ``Website 0.0.0.0``
* Click *fa-external-link* icon to edit the Website
* At **Website Domain** field copy-paste build domain and add something right after the first dot, for example::

      Original domain: 3308093-10-0-28910f.runbot2.odoo-community.org
           New domain: 3308093-10-0-28910f.second-website.runbot2.odoo-community.org

* Click ``[Save]`` to save changes at the Website
* Now you can use unchanged build domain for website called ``Website localhost`` and updated domain for website called ``Website 0.0.0.0``

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

Credits
=======

Contributors
------------

* Rafael Blasco <rafael.blasco@tecnativa.com>
* Antonio Espinosa <antonio.espinosa@tecnativa.com>
* Jairo Llopis <jairo.llopis@tecnativa.com>
* Ivan Yelizariev <https://it-projects.info/team/yelizariev>
* Dennis Sluijk <d.sluijk@onestein.nl>

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
