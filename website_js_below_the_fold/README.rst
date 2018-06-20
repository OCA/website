.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=========================
Website JS Below The Fold
=========================

This module moves Javascript assets to the bottom of the page (below the fold)
preventing your website having render-blocking Javascript.

When a visitor enters your website the browser will parse the HTML result.
Whenever the parser encounters a script, it has to load and execute the script before it can continue parsing.
So with render-blocking Javascript (e.g. in the head tag) the time to render the above the fold content increases.

Without render-blocking Javascript (by e.g. loading it below the fold) the page first render occurs faster.
This may result in various benefits e.g. lower bounce rate.

More information:

* `Render-blocking Javascript <https://developers.google.com/speed/docs/insights/BlockingJS>`_
* `Above the fold <https://en.wikipedia.org/wiki/Above_the_fold>`_

Usage
=====

This is a technical module and have no graphical interface whatsoever.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/11.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/website/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Dennis Sluijk <d.sluijk@onestein.nl>

Do not contact contributors directly about support or help with technical issues.

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
