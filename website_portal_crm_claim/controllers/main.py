# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import logging
from urllib import quote

from openerp import _
from openerp.http import request, route

_logger = logging.getLogger(__name__)

try:
    from openerp.addons.website_portal_v10.controllers.main \
        import WebsiteAccount as _Base
except ImportError:  # pragma: no-cover
    _Base = object
    _logger.info("Error importing `website_portal_v10`. Install it.")
    _logger.debug("Traceback:", exc_info=True)


class WebsiteAccount(_Base):
    @route()
    def account(self):
        """Add claims to main account page."""
        response = super(WebsiteAccount, self).account()
        Claim = request.env["crm.claim"]
        response.qcontext.update({
            "crm_claim_count": Claim.search_count([]),
        })
        return response

    @route(["/my/claims", "/my/claims/page/<int:page>"],
           type="http", auth="user", website=True)
    def portal_my_claims(self, page=1, date_begin=None, date_end=None,
                         **kwargs):
        values = self._prepare_portal_layout_values()
        Claim = request.env["crm.claim"]
        url = "/my/claims"
        mailto = False
        alias = (request.env["sale.config.settings"]
                 ._find_default_claim_alias_id())
        if "@" in alias.display_name and alias.alias_domain != "localhost":
            mailto = u"mailto:{alias.display_name}?subject={subject}".format(
                alias=alias,
                subject=quote(_("Claim for order # XXXXXX")),
            )

        # Get the domain for this view
        domain = list()
        archive_groups = self._get_archive_groups("crm.claim", domain)
        if date_begin and date_end:
            domain += [("message_last_post", ">=", date_begin),
                       ("message_last_post", "<", date_end)]

        # Count for pager
        count = Claim.search_count(domain)

        # Make pager
        pager = request.website.pager(
            url=url,
            url_args={"date_begin": date_begin, "date_end": date_end},
            total=count,
            page=page,
            step=self._items_per_page,
        )

        # Sarch the count to display, according to the pager data
        claims = Claim.search(
            domain, limit=self._items_per_page, offset=pager["offset"])

        values.update({
            "alias": alias,
            "mailto": mailto,
            "date": date_begin,
            "claims": claims,
            "pager": pager,
            "archive_groups": archive_groups,
            "default_url": url,
        })
        return request.website.render(
            "website_portal_crm_claim.portal_my_claims", values)

    @route(["/my/claims/<model('crm.claim'):claim>"],
           type="http", auth="user", website=True)
    def claims_followup(self, claim=None, **kwargs):
        return request.website.render(
            "website_portal_crm_claim.claims_followup",
            {"claim": claim})
