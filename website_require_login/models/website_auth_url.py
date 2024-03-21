# Copyright 2020 Advitus MB
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class WebsiteAuthURL(models.Model):
    _name = "website.auth.url"
    _description = "Authorization required URLs"

    website_id = fields.Many2one(
        comodel_name="website",
        required=True,
    )

    path = fields.Char(
        required=True,
        help=(
            "Relative URL path and subpath. "
            "Ex.: /shop will restrict /shop, /shop/product, etc."
        ),
    )

    _sql_constraints = [
        (
            "path_unique",
            "unique (website_id, path)",
            "The path must be unique per website!",
        )
    ]
