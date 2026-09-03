A portal customer editing one of their invoice or delivery addresses rewrites
the address in place. Documents issued with that address - confirmed orders,
posted invoices, delivery notes - then display an address they were never
issued with, and there is no trace of what it used to be.

This module makes the frontend create a new address instead, and leaves the
edited one untouched. The original address is not archived: it stays in the
address book and the customer can still use it.

Two cases are deliberately left alone: the customer's own contact record, which
is not an invoice or delivery address but their own data, and a form saved
without changing anything, which would otherwise leave a duplicate behind on
every visit.

Nothing else changes: core creates the new address, attaches it to the
commercial partner and returns it, so `website_sale` points the cart at it on
its own.
