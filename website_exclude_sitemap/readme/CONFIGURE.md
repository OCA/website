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

Paths without `*` are matched by equality after normalizing the trailing slash.
For example, `/customers/` excludes `/customers`, but it does not exclude
`/customers/other`.

Patterns with `*` use wildcard matching. For example, `/blog/*/feed` excludes
`/blog/other/feed`, but it does not exclude `/blog/feed/other`.

Use the **Reload Sitemap** button in the same settings block to clear the
cached sitemap manually.
