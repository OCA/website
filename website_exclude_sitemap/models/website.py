# Copyright 2026 Binhex <https://www.binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import re
from urllib.parse import urlsplit

from odoo import api, fields, models, tools

SITEMAP_DEFAULT_EXCLUDED_PATHS = (
    "/customers/",
    "/livechat",
    "/blog/*/feed",
    "/jobs/apply/",
    "/profile/",
)

SITEMAP_DEFAULT_EXCLUDED_PATHS_TEXT = "\n".join(SITEMAP_DEFAULT_EXCLUDED_PATHS)

SITEMAP_WILDCARDS = {"**": ".*", "*": "[^/]*"}


class Website(models.Model):
    _inherit = "website"

    sitemap_excluded_paths = fields.Text(
        string="Sitemap Exclusions",
        default=SITEMAP_DEFAULT_EXCLUDED_PATHS_TEXT,
        help=(
            "One path or pattern per line, comma, or semicolon. "
            "* matches inside one path segment, ** across segments, and a "
            "trailing / excludes a path and everything below it. "
            "Examples: /contactus, /solutions*, /blog/*/feed, /customers/, "
            "/jobs/**"
        ),
    )

    @staticmethod
    def _normalize_sitemap_path(value):
        """Return the path to compare, without its trailing slash."""
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

    @classmethod
    def _normalize_sitemap_pattern(cls, value):
        """Return the pattern, keeping the trailing slash that marks a prefix."""
        value = (value or "").strip()
        normalized = cls._normalize_sitemap_path(value)
        if normalized == "/" or not value.endswith("/"):
            return normalized
        return f"{normalized}/"

    @classmethod
    def _split_sitemap_patterns(cls, excluded_paths):
        """Split the raw exclusions text into normalized patterns."""
        return [
            cls._normalize_sitemap_pattern(pattern)
            for pattern in re.split(r"[\n,;]+", excluded_paths or "")
            if pattern.strip() and not pattern.lstrip().startswith("#")
        ]

    def _get_sitemap_excluded_patterns(self):
        self.ensure_one()
        return self._split_sitemap_patterns(self.sitemap_excluded_paths)

    @classmethod
    def _compile_sitemap_pattern(cls, pattern):
        """Compile an exclusion pattern into a regex matched against a path.

        ``*`` matches inside a single path segment, ``**`` crosses ``/``, and a
        pattern ending in ``/`` or in ``/**`` is a prefix: it matches that path
        and everything below it.
        """
        is_prefix = False
        if pattern.endswith("/**"):
            is_prefix = True
            pattern = pattern[: -len("/**")]
        elif pattern != "/" and pattern.endswith("/"):
            is_prefix = True
            pattern = pattern[:-1]
        body = "".join(
            SITEMAP_WILDCARDS.get(token, re.escape(token))
            for token in re.split(r"(\*\*|\*)", pattern)
        )
        return re.compile(f"^{body}(/.*)?$" if is_prefix else f"^{body}$")

    @tools.ormcache("excluded_paths")
    def _get_sitemap_excluded_regexes(self, excluded_paths):
        """Return the compiled patterns of the given raw exclusions text.

        The result is cached per database on the text itself, so the patterns
        are compiled once instead of once per sitemap entry.
        """
        return tuple(
            self._compile_sitemap_pattern(pattern)
            for pattern in self._split_sitemap_patterns(excluded_paths)
        )

    def _get_own_sitemap_excluded_regexes(self):
        self.ensure_one()
        return self._get_sitemap_excluded_regexes(self.sitemap_excluded_paths or "")

    def _is_sitemap_path_excluded(self, path):
        self.ensure_one()
        normalized_path = self._normalize_sitemap_path(path)
        return any(
            regex.match(normalized_path)
            for regex in self._get_own_sitemap_excluded_regexes()
        )

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
            self.env.registry.clear_cache()
            self._clear_sitemap_cache()
        return result

    def _enumerate_pages(self, query_string=None, force=False):
        """Drop the excluded URLs from the sitemap enumeration.

        ``force=True`` means the caller wants every page, not the sitemap
        listing: it is used by ``search_pages`` to feed the link autocomplete of
        the editor. The exclusions only apply to the sitemap, so that call is
        left untouched.
        """
        self.ensure_one()
        pages = super()._enumerate_pages(query_string=query_string, force=force)
        if force:
            yield from pages
            return
        regexes = self._get_own_sitemap_excluded_regexes()
        for page in pages:
            path = self._normalize_sitemap_path(page.get("loc"))
            if not any(regex.match(path) for regex in regexes):
                yield page
