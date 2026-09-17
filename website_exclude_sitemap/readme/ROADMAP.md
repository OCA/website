The exclusion list is a denylist evaluated after Odoo has collected every
sitemap source, so it only removes URLs, never adds them. When a record is
marked as indexed but its URL matches an exclusion pattern, the pattern wins and
the URL stays out of `/sitemap.xml`.

Nothing warns about that in the record itself: a page whose **Indexed** toggle is
on, or a published blog post, gives no hint that a global pattern is keeping it
out of the sitemap. The only place where the exclusions are visible is **Website
> Configuration > Settings**.

A future version could show the conflict where the record is edited, for example
a message next to the **Indexed** toggle of `website.page`. Covering models from
other modules, such as `blog.post`, belongs in bridge modules instead, to keep
this module depending on `website` alone.
