11.0.1.2.1 (Unreleased)
~~~~~~~~~~~~~~~~~~~~~~~

* Fix handling of request attribute
* Add backward compatibility for recent API refactoring

  [simahawk]

11.0.1.2.0 (2019-01-10)
~~~~~~~~~~~~~~~~~~~~~~~

* Refactor APIs and allow per-website config

  * API keys can now be configured via website settings
    which in turn allow to customize the values per website
    in a multi-website instance;

  * move all internal APIs to the model `website.form.recaptcha`
    so that we do not depend anymore on the controller
    if we need to integrate it into other pieces of code.

  * Use readme fragments

  [simahawk]


11.0.1.1.0 (2019-01-10)
~~~~~~~~~~~~~~~~~~~~~~~

* Improve JS and enforce translations

  Make JS modular and pass language parameter according to website lang.

  [mpanarin]

* Fix duplicated calls

  When website_crm_phone_validation is installed,
  the captcha validation is called twice
  so the form always fail as with a 'timeout-or-duplicate' error.

* Fix JS LINT errors

* Improve error handling to show all error messages at the same time

  [chienandalu]


11.0.1.0.0 (2017-10-30)
~~~~~~~~~~~~~~~~~~~~~~~

* Migrate to v11

  [dbo-odoo]
