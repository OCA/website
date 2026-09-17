Configure sitemap exclusions:

1. Go to **Website > Configuration > Settings**.
2. Locate the **Sitemap Exclusions** setting.
3. Enter one or more paths or glob patterns.
4. Save the settings.

Values can be separated by:

- line breaks;
- commas;
- semicolons.

For example, these values are equivalent:

```text
/customers/
/livechat
/blog/*/feed
/jobs/apply/
/profile/
```

```text
/customers/, /livechat, /blog/*/feed, /jobs/apply/, /profile/
```

```text
/customers/; /livechat; /blog/*/feed
/jobs/apply/, /profile/
```

Lines starting with `#` are comments.

See the usage section for the full pattern syntax: `*` matches inside one path
segment, `**` crosses `/`, and a pattern ending in `/` or in `/**` excludes that
path and everything below it.

The default value only covers paths that any Odoo website has. Add the paths
that are specific to your own deployment, for example:

```text
/website/info
/create-container-error
/machine-creation
```

`/website/info` is already left out of the sitemap by the core when its view is
inactive; add it here when that view stays active.

Use the **Reload Sitemap** button in the same settings block to clear the
cached sitemap manually.
