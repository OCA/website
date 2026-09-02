When ``website_cf_turnstile`` is installed, requests to
``/website_mail/follow`` are validated by Turnstile.

However, the follow widget provided by ``website_mail`` does not send the
``turnstile_captcha`` token, causing follow and unfollow operations to fail
with Cloudflare validation enabled.