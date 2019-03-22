.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================================
Configure search engine indexing for Odoo endpoints
====================================================

By default, /robots.txt on an Odoo installation with website module installed will allow indexing by webcrawlers.

This module will read the noindex parameter on the http.route decorator to generate a /robots.txt.

Installation
============

Just install the module.

Configuration
=============

Nothing special to be configured.

Usage
=====

For each http.route which should not be indexed, add the parameter ``"noindex"`` to the
route decorator.

The value of the parameter is a list of strings. The following values are used:

- ``"meta"`` add the tag <meta name="robots" content="noindex"/> to an html page
  (based on website.layout).
- ``"header"`` add the header 'X-Robots-Tag: noindex' to the http response.
- ``"robots"`` signals the robots.txt generator that the route should not be crawled.

.. code-block:: python

    @http.route(['/example_1'], type='http', auth="public", noindex=['robots'])
    def route_controller_1(self):
        pass

    @http.route(['/example_2'], type='http', auth="public",
                noindex=['robots', 'meta', 'header'])
    def route_controller_2(self):
        pass

Known issues / Roadmap
======================

- When two endpoints are resolved to the same wildcard URL, only the noindex
  information of the last endpoint parsed is used.
- Does not do any special works for multilang website.

Bug Tracker
===========

Credits
=======

Contributors
------------

* Christopher Meier <dev@c-meier.ch>
