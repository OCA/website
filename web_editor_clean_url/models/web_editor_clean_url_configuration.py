# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

import re
from urllib.parse import urlparse, urlunparse

from lxml import etree, html

from odoo import api, exceptions, fields, models


class WebEditorCleanUrlConfiguration(models.Model):
    _name = "web.editor.clean.url.configuration"
    _description = "Clean URLs configuration"
    _order = "sequence"

    active = fields.Boolean(default=True)
    sequence = fields.Integer()
    hostname = fields.Char(
        help="Fill in a domain to restrict this configuration to this domain",
    )
    query_parameter_separator = fields.Char(default="&")
    remove_query_parameter = fields.Char(
        help="Fill in comma separated query parameters to remove"
    )
    replace_regex = fields.Char(help="Fill in a regex applied to the whole URL")
    replace_regex_sub = fields.Char(
        "Substitution",
        help="Fill in a substitution for the regex above. \\1, \\2 etc contain matched "
        "content from brackets",
    )
    test_url = fields.Char(store=False)
    preview_url = fields.Char(compute="_compute_preview_url")

    @api.depends(lambda self: self._fields)
    def _compute_preview_url(self):
        for this in self:
            try:
                this.preview_url = (
                    this.test_url and this.clean_url(this.test_url) or False
                )
            except Exception as e:
                raise exceptions.ValidationError(e) from e

    @api.constrains(lambda self: (f for f in self._fields if self._fields[f].store))
    def _check_all(self):
        for this in self:
            try:
                # flake8 complains about missing whilespace after :
                this.clean_url(f"https://{this.hostname or 'test.com'}")  # noqa: E231
            except Exception as e:
                raise exceptions.ValidationError(e) from e

    def name_get(self):
        return [
            (
                this.id,
                this.hostname or this.remove_query_parameter or this.replace_regex,
            )
            for this in self
        ]

    def apply_all(self):
        """
        Apply configurations in self to all views
        """

        def html_fromstring(src):
            return html.fromstring(
                f"<div>{src}</div>", parser=html.HTMLParser(encoding="utf8")
            )

        def html_tostring(doc):
            return html.tostring(doc, encoding="utf8").decode("utf8")[5:-6]

        def xml_fromstring(src):
            return etree.fromstring(src)

        def xml_tostring(doc):
            return etree.tostring(doc, encoding="utf8").decode("utf8")

        IrUiView = self.env["ir.ui.view"]
        for records, fieldname in self._apply_all_get_records_and_field():
            if isinstance(records._fields[fieldname], fields.Html):
                fromstring = html_fromstring
                tostring = html_tostring
            else:
                fromstring = xml_fromstring
                tostring = xml_tostring

            for record in records:
                new_content = tostring(
                    IrUiView._web_editor_clean_url_clean_arch(
                        fromstring(record[fieldname]), configurations=self
                    )
                )
                if str(record[fieldname]) != new_content:
                    record[fieldname] = new_content

    def _apply_all_get_records_and_field(self):
        """
        Find all views and other records to apply a configuration on,
        return records, fieldname to be processed
        """
        result = []

        views_with_xmlid = self.env["ir.ui.view"].browse(
            self.env["ir.model.data"]
            .search([("model", "=", "ir.ui.view")])
            .mapped("res_id")
        )
        views = self.env["ir.ui.view"].search(
            [("type", "=", "qweb")]
        ) - views_with_xmlid.filtered(lambda x: not x.arch_updated)
        result.append((views, "arch_db"))

        if "blog.post" in self.env:
            result.append((self.env["blog.post"].search([]), "content"))
        if "event.event" in self.env:
            result.append((self.env["event.event"].search([]), "description"))
        if "product.template" in self.env:
            result.append((self.env["product.template"].search([]), "description"))

        return result

    def clean_url(self, url):
        """
        Clean url
        """
        if self._clean_url_ignore(url):
            return url
        parsed_url = urlparse(url)
        hostnames = list(map(str.strip, filter(None, (self.hostname or "").split(","))))
        hostnames += [("www." + hostname) for hostname in hostnames]
        if self.hostname and parsed_url.netloc not in hostnames:
            return url
        if self.remove_query_parameter:
            parameters = self._parse_query_parameters(parsed_url)
            for parameter in self.remove_query_parameter.split(","):
                parameters.pop(parameter.strip(), None)
            parsed_url = self._join_query_parameters(parsed_url, parameters)
        if self.replace_regex:
            parsed_url = urlparse(
                re.sub(
                    self.replace_regex,
                    self.replace_regex_sub or "",
                    urlunparse(parsed_url),
                )
            )
        return urlunparse(parsed_url)

    def _clean_url_ignore(self, url):
        """
        Return true if url shouldn't be rewritten
        """
        return url.startswith("#") or url.startswith("mailto:")

    def _parse_query_parameters(self, parsed_url):
        """
        Return a dict of parameters for parsed_url
        """
        result = {}
        if not parsed_url.query:
            return result
        for parameter_tuple in (parsed_url.query or "").split(
            self.query_parameter_separator
        ):
            split_parameter = parameter_tuple.split("=", 1)
            if len(split_parameter) > 1:
                name, value = split_parameter
            else:
                name = split_parameter[0]
                value = ""
            result[name] = value
        return result

    def _join_query_parameters(self, parsed_url, parameters):
        """
        Return a version of url with params replaced by parameters
        """
        return parsed_url._replace(
            query=self.query_parameter_separator.join(
                "=".join(parameter_tuple) for parameter_tuple in parameters.items()
            )
        )
