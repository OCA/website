# Copyright 2026 Binhex <https://www.binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import re
from urllib.parse import urlsplit

from odoo import api, fields, models

SITEMAP_DEFAULT_EXCLUDED_PATHS = (
    "/customers/",
    "/livechat",
    "/blog/*/feed",
    "/jobs/apply/",
    "/profile/",
    "/website/info",
    "/create-container-error",
    "/machine-creation",
)

SITEMAP_DEFAULT_EXCLUDED_PATHS_TEXT = "\n".join(SITEMAP_DEFAULT_EXCLUDED_PATHS)


class Website(models.Model):
    _inherit = "website"

    sitemap_excluded_paths = fields.Text(
        string="Sitemap Exclusions",
        default=SITEMAP_DEFAULT_EXCLUDED_PATHS_TEXT,
        help=(
            "One path or glob pattern per line, comma, or semicolon. "
            "Examples: /contactus, /shop*, /blog/*"
        ),
    )

    @staticmethod
    def _normalize_sitemap_path(value):
        value = (value or "").strip()
        if not value:
            return "/"
        if "://" in value:
            parsed = urlsplit(value)
            value = parsed.path or "/"
            if parsed.query:
                value = f"{value}?{parsed.query}"
        if not value.startswith("/"):
            value = f"/{value}"
        return "/" if value == "/" else value.rstrip("/")

    def _get_sitemap_excluded_patterns(self):
        self.ensure_one()
        return [
            self._normalize_sitemap_path(pattern)
            for pattern in re.split(r"[\n,;]+", self.sitemap_excluded_paths or "")
            if pattern.strip() and not pattern.lstrip().startswith("#")
        ]

    def _is_sitemap_path_excluded(self, path):
        self.ensure_one()
        normalized_path = self._normalize_sitemap_path(path)
        return any(
            self._matches_sitemap_pattern(normalized_path, pattern)
            for pattern in self._get_sitemap_excluded_patterns()
        )

    @staticmethod
    def _matches_sitemap_pattern(path, pattern):
        if "*" not in pattern:
            return path == pattern
        regex = f"^{'.*'.join(re.escape(part) for part in pattern.split('*'))}$"
        return re.match(regex, path) is not None

    def _clear_sitemap_cache(self):
        IrAttachment = self.env["ir.attachment"].sudo()
        for website in self:
            IrAttachment.search(
                [
                    ("type", "=", "binary"),
                    ("url", "=like", f"/sitemap-{website.id}-%"),
                ]
            ).unlink()

    @api.model_create_multi
    def create(self, vals_list):
        websites = super().create(vals_list)
        websites.filtered("sitemap_excluded_paths")._clear_sitemap_cache()
        return websites

    def write(self, vals):
        result = super().write(vals)
        if "sitemap_excluded_paths" in vals:
            self._clear_sitemap_cache()
        return result

    def _enumerate_pages(self, query_string=None, force=False):
        self.ensure_one()
        for page in super()._enumerate_pages(query_string=query_string, force=force):
            if not self._is_sitemap_path_excluded(page.get("loc")):
                yield page
