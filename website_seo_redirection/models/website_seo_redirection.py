# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.http import request, local_redirect
from odoo.exceptions import ValidationError
from ..exceptions import NoOriginError, NoRedirectionError


class WebsiteSeoRedirection(models.Model):
    _name = "website.seo.redirection"
    _rec_name = "destination"
    _order = "destination"
    _description = "SEO controller redirections"
    _sql_constraints = [
        ("origin_unique", "UNIQUE(origin)", "Duplicated original URL"),
        ("destination_unique", "UNIQUE(destination)", "Duplicated new URL"),
    ]

    origin = fields.Char(
        string="Original URL",
        required=True,
        index=True,
        help="Path where the original controller was found.",
    )
    destination = fields.Char(
        string="Redirected URL",
        required=True,
        index=True,
        help="Path where the controller will be found now.",
    )

    @api.multi
    @api.constrains("origin")
    def _check_origin(self):
        self._url_format_check("origin")

    @api.multi
    @api.constrains("destination")
    def _check_destination(self):
        self._url_format_check("destination")

    @api.multi
    def _url_format_check(self, field_name):
        display = self._fields[field_name].string
        for s in self:
            value = s[field_name]
            if not value.startswith("/"):
                raise ValidationError(_("%s must start with `/`") % display)
            for char in "?&=#":
                if char in value:
                    raise ValidationError(
                        _("Invalid character found in %s: `%s`") %
                        (display, char))
            if s.origin == s.destination:
                raise ValidationError(
                    _("You cannot redirect an URL to itself."))

    @api.model
    def find_origin(self, redirected_path=None):
        """Finds the original path for :param:`redirected_path`.

        :param str redirected_path:
            Destination path to get to a controller.

        :raise NoOriginError:
            When no original URL is found.

        :return str:
            Returns the original path (e.g. ``/page/example``) if
            :attr:`redirected_path` (e.g. ``/example``) is found among the SEO
            redirections, or :attr:`redirected_path` itself otherwise.
        """
        path = redirected_path or request.httprequest.path
        redirection = self.search([("destination", "=", path)])
        if not redirection.origin:
            raise NoOriginError(_("No origin found for this redirection."))
        return redirection.origin

    @api.model
    def redirect_auto(self, path=None, code=301, website=None, rerouting=None):
        """Return a redirection for the SEO path or fail.

        :param str path:
            Path that will be searched among the SEO redirections.

        :param int code:
            HTTP redirection code.

        :param website odoo.models.Model:
            Current website object. Default: ``request.website``.

        :param list rerouting:
            List of reroutings performed. It defaults to ``request.rerouting``.

        :raise NoRedirectionError:
            If no redirection target is found. This allows you to continue
            the normal behavior in your controller.

        :return werkzeug.wrappers.Response:
            Redirection to the SEO version of the URL.
        """
        # Default values
        path = path or request.httprequest.path
        rerouting = rerouting or getattr(request, "rerouting", list())
        website = website or getattr(
            request, "website", self.env["website"].get_current_website())

        # Search for a SEO destination
        match = self.search([("origin", "=", path)])
        destination = match.destination

        # Fail when needed
        if not destination:
            raise NoRedirectionError(_("No redirection target found."))
        if destination in rerouting:
            raise NoRedirectionError(_("Duplicated redirection."))

        # Add language prefix to URL
        if website.default_lang_code != request.lang:
            destination = u"/{}{}".format(request.lang, destination)

        # Redirect to the SEO URL
        return local_redirect(
            destination,
            dict(request.httprequest.args),
            True,
            code=code)
