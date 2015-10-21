Website Menu By User Status
===========================

The module manages display website menu entries, depending if the user is
logged or not.
The selection of the display status can be chosen logged and/or not.
Extends features and view of website.menu model.

Website.menu list view can be found at:
Settings > Configuration > Website Settings > Configure Website menus

The module inherit from website.menu to add 2 booleans fields, user_logged
and user_not_logged.
On top of that, website.layout template is extended to include a condition
that drive if the menu is built or not.
It has been choose to not only hide the menu to avoid to easily get around
by editing the html DOM.

Contributors
------------
* Bruno Joliveau <bruno.joliveau@savoirfairelinux.com>
* Jordi Riera <jordi.riera@savoirfairelinux.com>

More information
----------------
Module developed and tested with Odoo version 8.0
For questions, please contact our support services
<support@savoirfairelinux.com>
