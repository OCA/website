This module lets website administrators exclude public website URLs from
`/sitemap.xml`.

The module only affects sitemap generation. It does not unpublish pages, change
access rights, or block direct access to the excluded URLs.

It also clears the cached sitemap when website pages are created, deleted, or
their URL changes, so sitemap URLs are refreshed in the next sitemap generation.
