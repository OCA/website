# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    has_matomo_analytics = fields.Boolean("Matomo Analytics")
    matomo_analytics_id = fields.Integer(
        "Matomo website ID",
        help="The ID Matomo uses to identify the website",
        default=1,
    )
    matomo_analytics_host = fields.Char(
        "Matomo host",
        help="The host/path your Matomo installation is "
        "accessible by on the internet. Do not include a protocol here!\n"
        "So http[s]://[this field]/matomo.php should resolve to your matomo.php",
    )

    def _matomo_track_page_script(self):
        self.ensure_one()
        res = """
  var _paq = window._paq = window._paq || [];
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="%s";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '%s']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();""" % (
            self.matomo_analytics_host,
            self.matomo_analytics_id,
        )
        return res
