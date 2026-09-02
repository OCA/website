Hides the **Sign In** button from the website navigation bar.

The button is hidden via Bootstrap's `d-none` class so it remains in the
rendered HTML and can be restored simply by uninstalling this module.
Logged-in users are unaffected — their user menu is a separate element
rendered only when an authenticated session exists.

This module is useful when a website is purely public-facing and sign-in
access should not be advertised to visitors, while still allowing direct
access via `/web/login` for administrators.
