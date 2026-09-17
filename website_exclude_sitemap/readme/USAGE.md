Sitemap exclusions:

1. Create or publish website pages as usual.
2. Configure the paths or patterns to exclude in **Website > Configuration >
   Settings > Sitemap Exclusions**.

   ![Sitemap exclusions](../static/img/readme/config_sitemap_exclusions.png)

3. Open `/sitemap.xml`.
4. Confirm that excluded URLs are absent and non-excluded public pages are still
   present.

Pattern syntax:

| Pattern        | Matches                                                 | Does not match                     |
| -------------- | ------------------------------------------------------- | ---------------------------------- |
| `/livechat`    | `/livechat`                                             | `/livechat/room`                   |
| `/customers/`  | `/customers`, `/customers/acme`, `/customers/acme/2024` | `/customers-list`                  |
| `/blog/*/feed` | `/blog/news/feed`                                       | `/blog/a/b/feed`, `/blog/news`     |
| `/solutions*`  | `/solutions`, `/solutions-cloud`                        | `/solutions/cloud`                 |
| `/jobs/**`     | `/jobs`, `/jobs/apply/1`, `/jobs/a/b/c`                 | `/jobs-list`                       |

In short:

- `*` matches inside a single path segment; it never crosses a `/`.
- `**` crosses `/`, so it matches any number of segments.
- A pattern ending in `/` or in `/**` is a prefix: it excludes that path and
  everything below it.
- Any other pattern matches that exact path. The trailing slash of the URL is
  ignored, so `/livechat` and `/livechat/` are the same path.

Example:

- configure `/customers/`;
- publish a page at `/customers`;
- publish another page at `/customers/other`;
- open `/sitemap.xml`.

Both URLs are excluded, because `/customers/` is a prefix. Use `/customers`
without the trailing slash to exclude only the first one.

Ways to update the sitemap.xml:

1. The sitemap cache is automatically cleared when website pages are created or
   deleted, and when their URL, publication state, indexation, publication date
   or website changes.

2. The manual **Reload Sitemap** button can be used when a forced sitemap cache clear is
   needed.

   ![Reload manual sitemap](../static/img/readme/reload_manual_sitemap.png)
