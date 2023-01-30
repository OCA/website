To configure this module, you need to:

* go to Settings/General Settings/Website
* enable `Matomo Analytics`
* fill in `Matomo website ID` and `Matomo host`

At this point your website is already setup for being tracked in Matomo.

Some more advanced features offered by Matomo can be configured as follows:

User ID feature
~~~~~~~~~~~~~~~

Matomo includes a User ID feature for enhanced tracking on those websites that offer the ability for visitors to log in.
By tracking the User ID (unique identifier), it is possible to connect visitors between visits across multiple dates
and devices.

To enable this feature, set `Enable User ID`: Matomo will track the user's `ID` (model `res.users`).
If you want to use a different field, eg: user's `name` or `login`, you need to override method `compute_matomo_userid()`.

Enable a Heartbeat timer
~~~~~~~~~~~~~~~~~~~~~~~~

In order to better measure the time spent in the visit, the active page can send additional
ping requests to Matomo. These requests will not track additional actions or page views.
They just allow Matomo to know whether the user is actively viewing the page (the tab
should be active and in focus).

To enable this feature, set `Enable heartbeat` and define the Active Time.

By default, the Active Time is set to 15 seconds, meaning only if the page was viewed
for at least 15 seconds (and the user leaves the page or focuses away from the tab)
then a ping request will be sent.

Matomo Event Tracking
~~~~~~~~~~~~~~~~~~~~~

As explained in this page https://matomo.org/faq/reports/implement-event-tracking-with-matomo/
on the official documentation of Matomo, there are two main ways to set up event tracking within Matomo:

1. with the "Matomo Tag Manager" feature: this is the easiest and recommended way;
2. by adding snippets of JavaScript code to your website itself.

The first method is not supported by this module, however in OCA there's
a dedicated module for that purpose: `website_matomo_tag_manager`.

The second method can be used along with this module and requires a little more technical confidence.
You will need to integrate a JavaScript snippet directly into your website’s code.

Technical documentation can be found in:
https://developer.matomo.org/guides/tracking-javascript-guide#manually-trigger-events
