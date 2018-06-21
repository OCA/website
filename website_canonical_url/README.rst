.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=====================
Website Canonical URL
=====================

In Website Builder, eCommerce, Blog, etc. Odoo add parameters in URLs, like category,
page or sorting. This is a bad thing for SEO because it creates DUST (Duplicate URL,
Same Text) and Duplicate Content. That is to say, multiple URLs that leads to the same
page search engine's index.

This module doesn't prevent Odoo to generate such URLs, but it helps to reduce the
search engine's index size by adding canonical URLs for each page :
It insert a HTML tag in the html header
that contains a `canonical URL <https://support.google.com/webmasters/answer/139066>`_
for the current page, no matter what query string is.
Additionally you'll have `rel=next and rel=prev links 
<https://webmasters.googleblog.com/2011/09/pagination-with-relnext-and-relprev.html>`_
whenever a pager is found.


Configuration
-------------

Canonical URL is absolute. The domain name by default matches

"Settings / Technical / System Parameters / web.base.url"

This might not be enough to make sure that you have always one and only one URL
to access your resources.

You can force the domain by setting "Canonical domain" field into website settings.


How to verify
-------------

To check this on your website inspect the source of a page: 
you'll find canonical and prev/next "<link />" elements inside "<head />".

On a demo site (like Runbot) you can go to "/page/website_canonical_url.canonical_demo"
and inspect page's source.


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target:  https://runbot.odoo-community.org/runbot/186/10.0


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

* Thomas Rehn <thomas.rehn@initos.com>
* Rami Alwafaie <rami.alwafaie@initos.com>
* Jairo Llopis <jairo.llopis@tecnativa.com>
* Xavier Brochard <zeroheure@zeroheure.info>
* Simone Orsi <simone.orsi@camptocamp.com>

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
