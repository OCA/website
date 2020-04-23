In Website Builder, eCommerce, Blog, etc. Odoo add parameters in URLs, like category,
page or sorting. This is a bad thing for SEO because it creates DUST (Duplicate URL,
Same Text) and Duplicate Content. That is to say, multiple URLs that leads to the same
page search engine's index.

This module doesn't prevent Odoo to generate such URLs, but it helps to reduce the
search engine's index size by adding canonical URLs for each page :
It insert a HTML tag in the html header
that contains a `canonical URL <https://support.google.com/webmasters/answer/139066>`_
for the current page, no matter what query string is.
Additionally you'll have `rel=next and rel=prev links
<https://webmasters.googleblog.com/2011/09/pagination-with-relnext-and-relprev.html>`_
whenever a pager is found.
