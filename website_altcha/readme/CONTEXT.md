Currently, Odoo provides 2 options:

- Google Recaptcha relies on tracking of the user. It implies cookies
- Cloudfare Turnstile relies on signals of the browser so it is less GDPR problematic.
  However, it relies on a third party infrastructure. 
  The decision is made from a probabilistic perspective (likely a human)

With this new module, everything relies on our own system with no cookies, no tracking and no network calls.

The way to solve it is to add a deterministic puzzle to solve. 
Bots need to spend more CPU, making it costly at scale.
