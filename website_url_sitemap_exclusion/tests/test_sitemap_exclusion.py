#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime
from unittest.mock import patch

from odoo import tests
from odoo.addons.website.controllers.main import Website
from odoo.addons.website.tools import MockRequest
from odoo.exceptions import ValidationError
from odoo.tests import Form


class TestSiteMapExclusion (tests.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = Website()
        cls.website = cls.env['website'].browse(1)
        cls.sitemap = cls._get_sitemap(cls.env)

    @classmethod
    def _get_sitemap(cls, env):
        """Get the updated sitemap.

        Usually the sitemap is cached for 12 hours,
        here we reset the cache so that the sitemap returned is always updated.
        """
        base_url = cls.env['ir.config_parameter'].sudo().get_param('web.base.url')

        sitemap_cache_duration_path = 'odoo.addons.website' \
                                      '.controllers.main.SITEMAP_CACHE_TIME'
        no_cache = datetime.timedelta(seconds=-1)
        with patch(sitemap_cache_duration_path, new=no_cache), \
                MockRequest(env, website=cls.website) as request:
            request.httprequest.url_root = base_url
            cls.controller.sitemap_xml_index()
            # Sitemap content is the first parameter
            # of the first call to `make_response`
            sitemap = request.make_response.call_args[0][0]
        return sitemap

    def test_url_exclusion(self):
        """URLs defined in the Website are excluded from the sitemap."""
        # Arrange: We want to exclude a URL
        url_to_exclude = '/aboutus'
        url_regex = '/aboutus'
        sitemap = self.sitemap
        # pre-condition: The URL is in the sitemap,
        # and the regex matches the URL
        self.assertRegex(url_to_exclude, url_regex)
        self.assertIn(url_to_exclude, sitemap.decode())

        # Act: Exclude the URL in the website
        website_form = Form(self.website)
        with website_form.forbidden_url_ids.new() as forbid:
            forbid.regex = url_regex
        website_form.save()

        # Assert: The sitemap does not contain the URL
        new_sitemap = TestSiteMapExclusion._get_sitemap(self.env)
        self.assertNotIn(url_to_exclude, new_sitemap.decode())

    def test_not_valid_regex(self):
        """Only valid Regular Expressions can be used."""
        # Arrange: A Regular Expression is not valid
        not_valid_regex = '/abo[utus'

        # Act: Add the Regular Expression to the website forbidden URLs
        website_form = Form(self.website)
        with website_form.forbidden_url_ids.new() as forbid:
            forbid.regex = not_valid_regex
        with self.assertRaises(ValidationError) as ve:
            website_form.save()
        exc_message = ve.exception.args[0]

        # Assert: The validation error mentions the wrong Regular Expression
        self.assertIn(not_valid_regex, exc_message)
        self.assertIn('not valid', exc_message)
