To use this module:

  * Go to Website -> Pages and select a page to optimize
  * Clear out any current contents of the 'Critical CSS' field
  * Find out the public facing URL of this page
  * Generate Critical CSS for this URL while selecting the right widths for
    Desktop and Mobile views
  * Paste the blob in the 'Critical CSS' field.

To generate critical CSS you have a couple of options:

  * Use a free online Critical CSS generator. At the time of writing
    there are: Sitelocity, Pegasaas, web.dev, Corewebvitals.io, ...
  * Install the npm [critical](https://github.com/addyosmani/critical)
    package and generate it on your local.

To test improvement of FCP score, use for example Lighthouse, which is
build into Chrome browser.
