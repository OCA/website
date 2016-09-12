# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from psycopg2 import IntegrityError

from openerp import _, api, fields, models
from openerp.http import local_redirect, request
from openerp.exceptions import ValidationError

from ..exceptions import NoOriginError, NoRedirectionError


class WebsiteSeoRedirection(models.Model):
    _name = "website.seo.redirection"
    _rec_name = "destination"
    _order = "destination"
    _description = "SEO controller redirections"
    _sql_constraints = [
        ("origin_unique", "UNIQUE(origin)", "Duplicated original URL"),
        ("origin_destination_distinct",
         "CHECK(origin != destination)",
         "Recursive redirection."),
    ]

    origin = fields.Char(
        string="Original URL",
        required=True,
        index=True,
        help="Path where the original controller was found.",
    )
    destination = fields.Char(
        string="Destination URL",
        required=True,
        index=True,
        help="Path where the controller will be found now.",
    )
    relocate_controller = fields.Boolean(
        default=True,
        help="If you relocate the controller, the same page that was found in "
             "the original URL will be now in the destination. Otherwise, "
             "this will simply make requests be redirected, but a new "
             "controller should be available in the destination URL if you "
             "do not want a 404 error.",
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
    @api.constrains("origin", "destination")
    def _check_not_recursive(self):
        """Avoid infinite loops."""
        for redirection in self:
            origins = {redirection.origin}
            while redirection:
                redirection = self.search([
                    ("origin", "=", redirection.destination),
                ])
                if redirection.origin in origins:
                    raise ValidationError(
                        _("Recursive redirection is forbidden."))
                origins.add(redirection.origin)

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
            When no original URL is found, or the found URL is not marked with
            :attr:`relocate_controller`.

        :return str:
            Returns the original path (e.g. ``/page/example``) if
            :attr:`redirected_path` (e.g. ``/example``) is found among the SEO
            redirections, or :attr:`redirected_path` itself otherwise.
        """
        path = redirected_path or request.httprequest.path
        redirection = self.search([
            ("destination", "=", path),
            ("relocate_controller", "=", True),
        ])
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

        :param website openerp.models.Model:
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
        if (website.default_lang_code != request.lang and
                request.lang in website.language_ids.mapped("code")):
            destination = u"/{}{}".format(request.lang, destination)

        # Redirect to the SEO URL
        return local_redirect(
            destination,
            dict(request.httprequest.args),
            code=code)

    @api.model
    def smart_add(self, origin, destination):
        """Add or update redirection only if needed.

        :param str origin:
            The original URL.

        :param str destination:
            The new redirected URL.
        """
        if origin == destination:
            return
        records = self.search([
            "|", ("origin", "=", origin),
            ("destination", "in", [origin, destination]),
        ])
        if records:
            for record in records:
                try:
                    with self.env.cr.savepoint():
                        record.destination = destination
                except (ValidationError, IntegrityError):
                    record.unlink()
        else:
            self.create({
                "origin": origin,
                "destination": destination,
            })
