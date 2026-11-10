To configure this module, you need to:

1.  Go to **Website \> Configuration \> Settings**
2.  Search 'Cookiefirst' option.
3.  Enable Use Cookiefirst checkbox
4.  Enter your Cookiefirst **API Key** into **Cookiefirst ID** field (e.g.
    '00000000-0000-0000-0000-000000000000').
5.  Click on "Save" button.

Configure a domain for each website and register that domain in CookieFirst.
The consent script is loaded only when both the domain and CookieFirst ID
are configured. Each website uses its own identifier.

Disable Odoo's native cookies bar when CookieFirst is enabled. In the
CookieFirst dashboard, enable Google Consent Mode and its default consent
settings, with the required consent types denied before a visitor chooses.
Do not pre-execute the performance category. See the
[CookieFirst Consent Mode configuration guide](https://cookiefirst.com/docs/troubleshoot-and-fix-google-consent-mode/).

CookieFirst controls both Google Analytics (`G-`) and Google Tag Manager
(`GTM-`), including their initialization scripts, through the performance
category. Do not install a second copy of the Google tags or CookieFirst
through Tag Manager. Check rejection, acceptance and withdrawal of consent
with your published CookieFirst configuration.

Disabling CookieFirst clears the website's identifier and restores Odoo's
native tracking behavior. Reconfigure the native cookies bar as required.
Upgrades preserve the existing identifier and the customized declaration
page at `/legal/cookies-policy`.

⚠️ **Please note: if another cookie consent solution is
installed (e.g. Cookiebot), the execution of the Cookiefirst
script will be prevented. Make sure that no other cookie
consent solution is installed when using the Cookiefirst module.**
