.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============
Cookie notice
=============

This module adds the cookie notice, according to the `european cookie law
<http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32002L0058:en:HTML>`_,
to your website.

=============
Configuration
=============

To change the cookie message:

* Go to *Settings > Technical > User Interface > Views*.
* Search for the view called *cookiebanner*.
* Change as you wish. Remember that you will probably lose translations then.

If you are developing a theme for Odoo, remember that this message has the
``cc-cookies`` class. You can style it at will too.

======================
Known Issues / Roadmap
======================

* If you are using this module in version < 8.0.2.0.0 and update it, any other
  module that modifies the ``res.company`` view will break in the next update
  if Odoo decides to update it before this one. To avoid that:

  1. Stop your server.
  2. Update only this module: ``odoo.py -u website_cookie_notice``.
  3. Stop your server.
  4. Update all other modules: ``odoo.py -u all``.
  5. Start your server.

* Before version 8.0.2.0.0 of this module, users had the ability to configure
  the message functionality and appearance from the main company form.

  Now, the message is generated in a view. This means that after upgrading to
  >= 8.0.2.0.0 you will lose your previous customized messages. If you want to
  customize it, please follow steps in the configuration section.

===========
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

* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Nicola Malcontenti <nicola.malcontenti@agilebg.com>
* Rafael Blasco <rafabn@antiun.com>
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

To contribute to this module, please visit http://odoo-community.org.