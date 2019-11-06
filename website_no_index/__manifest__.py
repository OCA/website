{
    'name': "website_no_index",
    'summary': """
        Choose which http.route must not be indexed by search engines.
    """,
    'description': """
        Add an option in the http.route decorator to allow the configuration of
        noindex information for search engine crawler.

        Supports 3 ways of refusing indexation:
        - Using the noindex meta tag in html pages.
        - Using the X-Robots-Tag header in http responses.
        - Adding the route in the robots.txt file.
    """,
    'author': 'Compassion CH',
    'license': 'AGPL-3',
    'website': 'http://www.compassion.ch',
    'category': 'Website',
    'version': '12.0.0.1.0',
    'depends': [
        'website',
    ],
    'installable': True,
    'data': [
        'views/robots.xml',
        'views/meta_tag.xml',
    ],
}
