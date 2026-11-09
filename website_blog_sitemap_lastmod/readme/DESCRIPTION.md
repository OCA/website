This module adds a trustworthy ``<lastmod>`` to ``blog.post`` URLs in the sitemap.

## Why it matters

Odoo core only emits ``lastmod`` for static ``website.page`` records. Dynamic controller routes, including blog posts, are listed in the sitemap without a modification date. Search engines use ``lastmod`` to decide how often to crawl a URL, so missing it can make crawl budgets less efficient.

## What it does

This module overrides ``website._enumerate_pages()`` and injects ``lastmod`` for every published ``blog.post`` URL. The date comes from the record ``write_date``, which is reliable for posts because all renderable content lives on the record itself.

Only the sitemap output changes; the public routes and their behaviour remain untouched.

## Technical notes

The override preloads a ``{url: lastmod}`` map for all published posts in a single query, then enriches matching pages during the normal enumeration. This keeps the sitemap generation efficient and follows the same core pattern used by ``website_forum``.
