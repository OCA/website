Website CRM Contact Mandatory Phone Number
==========================================
This module set as required the phone number in the form of the
"Contact Us" page.

8th September 2014: As the way website_crm controller is build, there is no
easy way to set a field as required in the controller. Because of that,
the method had to be copied, breaking the link with any update that would be
done on this part of code.

For now, instead of overcharging the field in the controller, the field is set
as required in the view. It is weak as the behaviour won't be the same if the
field is called from another view.

Contributors
------------

* Jordi RIERA <jordi.riera@savoirfairelinux.com>
* William BEVERLY <william.beverly@savoirfairelinux.com>
* Bruno JOLIVEAU <bruno.joliveau@savoirfairelinux.com>

More information
----------------

Module developed and tested with Odoo version 8.0
For questions, please contact our support services <support@savoirfairelinux.com>
