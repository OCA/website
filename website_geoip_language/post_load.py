# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging

import babel.core

from odoo import http
from odoo.tools.func import lazy_property

_logger = logging.getLogger(__name__)


def post_load():
    """
    Parsing country code into language code is copied from:
    https://github.com/OCA/OCB/blob/01b012346f25842c35be1bbe184e455cc00259c7/odoo/http.py#L1316
    """
    _logger.info(
        "website_geoip_language: Monkey patching http.Request.best_lang"
        " to use GeoIP resolved language."
    )
    _best_lang_orig = http.Request.best_lang

    @lazy_property
    def _best_lang_from_geoip(self):
        ip_lang = None
        best_lang = _best_lang_orig.__get__(self, cls=http.Request)
        geoip_resolve = http.Request._geoip_resolve(self)
        if geoip_resolve and geoip_resolve.get("country_code"):
            country_code = geoip_resolve["country_code"]
            try:
                code, territory, _, _ = babel.core.parse_locale(country_code, sep="-")
                if territory:
                    lang = f"{code}_{territory}"
                else:
                    lang = babel.core.LOCALE_ALIASES[code]
                ip_lang = lang
            except (ValueError, KeyError):
                _logger.warning(
                    "website_geoip_language: Could not parse country code %s",
                    country_code,
                )
        return ip_lang or best_lang

    http.Request.best_lang = _best_lang_from_geoip
