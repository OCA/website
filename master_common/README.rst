.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

====================
Antiun Master common
====================

This module is a master addon for installing and configuring a vertical solution

It depends on those addons:

* `OCA/web <https://github.com/OCA/web/tree/8.0>`_ :
    * `support_branding <https://github.com/OCA/web/tree/8.0/support_branding>`_
    * `web_advanced_search_x2x <https://github.com/OCA/web/tree/8.0/web_advanced_search_x2x>`_
    * `web_sheet_full_width <https://github.com/OCA/web/tree/8.0/web_sheet_full_width>`_
    * `web_dialog_size <https://github.com/OCA/web/tree/8.0/web_dialog_size>`_
    * `web_translate_dialog <https://github.com/OCA/web/tree/8.0/web_translate_dialog>`_
    * `web_tree_many2one_clickable <https://github.com/OCA/web/tree/8.0/web_tree_many2one_clickable>`_
    * `web_m2x_options <https://github.com/OCA/web/tree/8.0/web_m2x_options>`_

* `OCA/server-tools <https://github.com/OCA/server-tools/tree/8.0>`_ :
    * `disable_openerp_online <https://github.com/OCA/server-tools/tree/8.0/disable_openerp_online>`_
    * `base_export_manager <https://github.com/OCA/server-tools/tree/8.0/base_export_manager>`_
    * `mass_editing <https://github.com/OCA/server-tools/tree/8.0/mass_editing>`_
    * `auth_signup_verify_email <https://github.com/OCA/server-tools/tree/8.0/auth_signup_verify_email>`_

* `OCA/social <https://github.com/OCA/social/tree/8.0>`_ :
    * `mail_attach_existing_attachment <https://github.com/OCA/social/tree/8.0/mail_attach_existing_attachment>`_
    * `mail_compose_select_lang <https://github.com/OCA/social/tree/8.0/mail_compose_select_lang>`_
    * `mail_mandrill <https://github.com/OCA/social/pull/18>`_ (PR #18 merge pending)
    * `mail_forward <https://github.com/OCA/social/tree/8.0/mail_forward>`_
    * `mail_full_expand <https://github.com/OCA/social/tree/8.0/mail_full_expand>`_
    * `mail_sent <https://github.com/OCA/social/tree/8.0/mail_sent>`_

* `Antiun/antiun-odoo-addons <https://github.com/Antiun/antiun-odoo-addons/tree/8.0>`_ :
    * `instance_watermark <https://github.com/Antiun/antiun-odoo-addons/tree/8.0/instance_watermark>`_

And automatically configure this system parameters for Antiun Ingeniería:

* support_branding.company_name
* support_branding.company_url
* support_branding.company_color
* support_branding.support_email
* support_branding.release
* web_tree_many2one_clickable.default
* web_m2x_options.create

**IMPORTANT NOTE**: support_branding.* parameters are overwritten with every update, but web_tree_many2one_clickable.default and web_m2x_options.create not.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/Antiun/antiun-odoo-addons/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/Antiun/antiun-odoo-addons/issues/new?body=module:%20master_common%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Rafael Blasco <rafabn@antiun.com>
* Antonio Espinosa <antonioea@antiun.com>


Maintainer
----------

.. image:: http://www.antiun.com/images/logo.png
   :alt: Antiun Ingeniería S.L.
   :target: http://www.antiun.com

This module is maintained by Antiun Ingeniería S.L.

Antiun Ingeniería S.L. is an IT consulting company especialized in Odoo
and provides Odoo development, install, maintenance and hosting
services.

To contribute to this module, please visit https://github.com/Antiun
or contact us at comercial@antiun.com
