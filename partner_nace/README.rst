.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

NACE Activities in Partner
==========================

This module adds the concept of NACE activity to the partner.

NACE is the Statistical Classification of Economic Activities in the European
Community. More info at http://ec.europa.eu/eurostat/en/web/products-manuals-and-guidelines/-/KS-RA-07-015

Allows you to select in partner form:

* Main NACE activity in a dropdown (many2one)
* Secondary NACE activities in a multi label input (many2many)

This addon is inspired in OCA/community-data-files/l10n_eu_nace, but it does
not use partner categories to assign NACE activities to partner.


Installation
============

To install this module, you need request python module:

* pip intall requests


Configuration
=============

After installation, you must click at import wizard to populate NACE items
in Odoo database in:
Sales > Configuration > Address Book > Import NACE Rev.2 from RAMON

This wizard will download from Europe RAMON service the metadata to
build NACE database in Odoo in all installed languages.

If you add a new language (or want to re-build NACE database), you should call
import wizard again.


Usage
=====

Only Administrator can manage NACE activity list (it is not neccesary because
it is an European convention) but any registered user can read them,
in order to allow to assign them to partner object.

After configuration, all NACE activities are available to be selected in
partner form as main and secondary activities.

Applies only to partners marked as companies


Known issues / Roadmap
======================

* Improve import algorithm: Use context lang key to translate NACE items


Credits
=======

Contributors
------------
* Antonio Espinosa <antonioea@antiun.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
