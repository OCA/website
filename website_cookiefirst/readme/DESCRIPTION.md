This module integrates Odoo website with GDPR through the functionality
of Cookiefirst (https://cookiefirst.com), you need to register your
website domain in Cookiefirst's portal.

Odoo only holds back its optional cookies (for example the `odoo_utm_*`
campaign cookies) while its own cookie bar is enabled. With Cookiefirst
the Odoo cookie bar is off, so this module makes optional cookies follow
the visitor's Cookiefirst choice instead: they are only set once the
*Performance* category is accepted. Without a choice, after a rejection,
or with an unreadable consent cookie, they are not set.
