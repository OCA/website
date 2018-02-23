.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

========================
Claims in Website Portal
========================

This module extends the functionality of CRM claims to support showing them in
your portal users' website account page, and to allow them to send messages
from there or create new claims by sending an email to an automatically created
alias.

Configuration
=============

To configure this module, you need to:

#. Go to *Sales > Configuration > Settings*.
#. Change the *Claims Email Alias* field to whatever alias you want for claims.
   It defaults to ``claims``.

Usage
=====

To use this module, you need to:

#. Log in as a portal user.
#. Visit `your home </my/home>`_.
#. Enter `your claims </my/claims>`_. There you have the instructions to create
   a new claim, and the list of claims where you are subscribed.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/186/9.0

Known issues / Roadmap
======================

* ``website_crm_claim`` addon is a very ugly addon that just adds a link to
  backend portal of claims. It is in the dependency tree because it would get
  autoinstalled anyway, so this way we benefit from its security rules and can
  disable that link to the backend portal, but in v10, where all the
  ``crm.claim`` stuff has been removed in favor of the helpdesk, we should just
  import the security rules here and drop the other addon (or rename it to
  ``portal_crm_claim``).

* It would be nice to allow creating claims from a form instead of only by
  sending an email.

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
