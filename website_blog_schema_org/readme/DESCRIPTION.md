This module adds structured `schema.org/BlogPosting` JSON-LD metadata to every published Odoo Website blog post.

## Why it matters

Search engines understand HTML, but they understand structured data even better. By embedding a JSON-LD block in each blog post, you help Google and other crawlers surface rich results such as headline, author, publication date, modification date, publisher and featured image.

The module does not change the visual design of your blog; it only injects an invisible `<script type="application/ld+json">` block that uses the content you already maintain in Odoo.

## What is injected

The JSON-LD block is generated from the blog post record and includes:

* `@type`: `BlogPosting`
* `headline`: post name
* `url` and `mainEntityOfPage`: canonical post URL
* `datePublished`: post date
* `dateModified`: last modification date
* `author`: name of the post author
* `publisher`: website name and logo
* `inLanguage`: current environment language
* `image`: OpenGraph image when available

## Technical notes

The module inherits `blog.post` and adds `_get_article_jsonld()`. This method builds a Python dictionary following the schema.org `BlogPosting` vocabulary, serialises it with `json.dumps(..., ensure_ascii=False)` and returns it wrapped in `markupsafe.Markup` so Odoo renders it as safe HTML.

The template inherits `website_blog.blog_post_complete` and injects the script block right before `<section id="o_wblog_post_top">` using `t-out`.
