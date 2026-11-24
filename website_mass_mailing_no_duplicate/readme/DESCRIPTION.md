This module extends the ``website`` and ``mass_mailing`` Odoo modules to prevent
duplicates entries in ``mailing.contact`` tables.

**Rational**

In Odoo website, if the page contains Customer Form type = 'Subscribe to one (or many) newsletters', the form creates a new mailing.contact.
That can generate annoying duplicates.

This module prevent such duplicated entries, updating existing mailing.contact, if exists.
