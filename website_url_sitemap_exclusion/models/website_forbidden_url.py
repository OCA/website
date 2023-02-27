#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class WebsiteForbiddenUrls(models.Model):
    _name = "website.forbidden.url"
    _description = "URL not allowed in the sitemap"
    _rec_name = 'regex'

    regex = fields.Char(
        string="Regular Expression",
        required=True,
    )
    website_id = fields.Many2one(
        comodel_name="website",
        ondelete="cascade",
    )

    @api.constrains(
        'regex',
    )
    def constrain_regex_valid(self):
        """RegEx must be valid."""
        for forbidden_url in self:
            regex = forbidden_url.regex
            try:
                re.compile(regex)
            except re.error as error:
                raise ValidationError(
                    _("Regular Expression `{regex}` is not valid:\n"
                      "{error}")
                    .format(
                        regex=regex,
                        error=error.msg,
                    )
                ) from error
