# Improve the email password reset flow

- STATUS: CLOSED
- PRIORITY: 70
- TAGS: feature, security, email, ux

The email password reset flow is Django's stock implementation bolted onto
the existing phone (SMS/OTP) reset flow. It looks unfinished next to the phone
flow: the email is a minimal plain-text blob with generic English copy, the
POST endpoint has no rate limiting (the phone flow rate-limits everything),
the reset-link lifetime is Django's hard-coded 3-day default, and the whole
flow is always reachable even though the admin may never have configured an
SMTP server. Two pages are broken for realistic use: an invalid/expired reset
link crashes `password_reset_confirm.html` (Django passes `form=None` and the
template dereferences it), and the confirm page shows nothing about who the
link belongs to.

Decisions (confirmed with the product owner):

- Email counts as "set up" when the configured mail backend is a real sending
  backend (SMTP), not the dev `console` backend.
- When email is NOT set up, the four email-reset URLs must return 404 and all
  frontend links to the flow must be hidden.
- Make it "more real": branded HTML email, Persian subject, polished pages,
  rate limiting, configurable expiry.
- Do NOT touch the phone reset links in this task (they are gated separately).

Requirements:

- Add `is_email_setup()` helper (new module, e.g. `src/services/emailing.py`)
  that returns True when the effective mail backend is configured for sending.
  The effective backend must be read from `MAILERS["default"]["BACKEND"]`
  (Django 6.1's `MAILERS` setting governs actual sending; `EMAIL_BACKEND` is
  not authoritative and cannot be overridden with `override_settings` for
  sending) and compared against the console backend.
- Gate all four email-reset URLs (`password_reset`, `password_reset_done`,
  `password_reset_confirm`, `password_reset_complete`) behind
  `is_email_setup()`: raise `Http404` from the view `dispatch` when not set
  up. Replace the bare `auth_views.as_view(...)` wiring in `src/services/urls.py`
  with project views that subclass the Django auth views and add the gating
  mixin.
- Rate-limit the reset POST with `@ratelimit(key="ip", rate="5/m",
  method="POST", block=True)`, matching the phone flow. Empirically the
  project's `block=True` responses come back as HTTP 403.
- Make `PASSWORD_RESET_TIMEOUT` configurable via env (`config(..., default=259200, cast=int)`).
- Branded HTML email:
  - New inline-styled, RTL, Persian HTML template (e.g.
    `password_reset_email.html`) with the reset-link button, site branding,
    "if you did not request this" note, and team signature.
  - Plain-text fallback template (e.g. `password_reset_email.txt`) with the
    reset URL.
  - Persian subject template (e.g. `password_reset_subject.txt`).
  - Wire via `html_email_template_name` / `email_template_name` /
    `subject_template_name` on the custom `PasswordResetView` subclass (Django
    attaches the HTML part automatically via `EmailMultiAlternatives`).
- Polished pages:
  - `password_reset_confirm.html` must render a friendly "link invalid or
    expired" state when `validlink` is False (currently it crashes on
    `form=None`) with a link to request a new reset.
  - `password_reset_done.html` hint about checking spam/junk.
  - Minor copy polish on `password_reset_form.html` / complete page if needed.
- Hide references when email is not set up:
  - A context processor flag `email_reset_enabled` (from `is_email_setup()`).
  - `password_reset_phone_form.html` "بازیابی با ایمیل" link wrapped in
    `{% if email_reset_enabled %}`.
- Update `.env.example` (document `PASSWORD_RESET_TIMEOUT`) and README
  (mention the email reset feature and the backend-based gating).
- Tests (pytest, run in the Docker container):
  - Existing `TestPasswordReset` tests must switch to a locmem backend via
    `override_settings(MAILERS={"default": {"BACKEND": ...locmem..., "OPTIONS": {}}})`
    so they remain reachable and `mail.outbox` is populated.
  - All four URLs return 404 when email is not set up (default console).
  - All four URLs reachable when a sending backend is configured.
  - Phone reset page hides the email link when disabled and shows it when enabled.
  - Reset email has the Persian subject, an HTML alternative, and the reset URL.
  - Full end-to-end flow: submit email, read the token from `mail.outbox`,
    open the confirm link, set a new password, log in with it.
  - Rate limit: 6th POST returns 403 (clear the rate-limit cache first).
  - Expiry: with `PASSWORD_RESET_TIMEOUT` overridden (e.g. 0), a freshly
    generated token renders the invalid-link state (deterministic, no sleeps).

Design decisions:

- New module `src/services/emailing.py` for `is_email_setup()` so views,
  context processors, and tests share one definition.
- Email-setup rule: "not set up" == the `console` backend (the dev default).
  Any explicitly chosen backend (SMTP in production, locmem in tests) counts
  as set up, which keeps the tests able to assert against `mail.outbox`.
- Custom auth-view subclasses in `src/services/views.py` (next to the phone
  reset views) with a shared `_EmailResetRequiredMixin` for the 404 gating and
  `@method_decorator(ratelimit(...), name="dispatch")` for the rate limit.
- The confirm template must branch on `validlink` because Django sets
  `form=None` for invalid/expired tokens.

Done:

- Implemented. Full suite green (911 passed) and pre-commit clean.
- `src/services/emailing.py`: `is_email_setup()` reading the effective backend
  from `MAILERS["default"]["BACKEND"]` (console backend => not set up).
- `src/services/views.py`: `_EmailResetRequiredMixin` raising Http404 when not
  set up, plus `EmailResetView` (rate limited `5/m` per IP on POST) and the
  done/confirm/complete subclasses; `src/services/urls.py` rewired to them.
- `src/agahyar_project/settings.py`: `PASSWORD_RESET_TIMEOUT` via env;
  `email_features_context` registered and exposing `email_reset_enabled`.
- Email templates: `password_reset_subject.txt` (Persian subject),
  `password_reset_email.txt` (plain-text fallback),
  `password_reset_email.html` (branded inline-styled RTL HTML with button).
- `password_reset_confirm.html` renders a friendly invalid-link state when
  `validlink` is False (previously it crashed on `form=None`).
- `password_reset_phone_form.html` hides the email link unless enabled.
- Note: pytest-django auto-configures `MAILERS` to the locmem backend (so
  email is "set up" under tests by default) and `services.test_plugin` disables
  rate limiting; the tests override both explicitly where needed.

