Variable period for memberships
===============================

Current membership module allows to set products that define a fixed period
for a membership. This is good when the quotas are defined periodically, and
when you become a member, you are until the end of that quota cycle.

But a lot of times, membership quotas express an amount of time that you
gain the membership. For example, one year since the subscription.


This module allows to make it in Odoo, using current membership features,
and adapting them for this purpose. As now the quota is not attached to a fixed
period, you can also invoice more than one quantity for being a member for
the corresponding number of periods.

Finally, a cron has been included that triggers the recalculation of the
membership state, allowing to have "old members", which doesn't work well
on standard.

Usage
=====

Define a member product, and select 'Variable periods' in the field
*Membership type*. You will be able to select them the period for the
membership in quantity and interval.

Credits
=======

Contributors
------------

* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>

Icon
----

Original clipart from:

* http://pixabay.com/es/en-contacto-con-tarjeta-de-cr%C3%A9dito-97574/
* https://openclipart.org/detail/23920/sandglass

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
