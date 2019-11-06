For each http.route which should not be indexed, add the parameter ``"noindex"`` to the
route decorator.

The value of the parameter is a list of strings. The following values are used:

- ``"meta"`` add the tag <meta name="robots" content="noindex"/> to an html page
  (based on website.layout).
- ``"header"`` add the header 'X-Robots-Tag: noindex' to the http response.
- ``"robots"`` signals the robots.txt generator that the route should not be crawled.

.. code-block:: python

    @http.route(['/example_1'], type='http', auth="public", noindex=['robots'])
    def route_controller_1(self):
        pass

    @http.route(['/example_2'], type='http', auth="public",
                noindex=['robots', 'meta', 'header'])
    def route_controller_2(self):
        pass

