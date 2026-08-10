"""Email readiness helpers for the Agahyar project.

The project only sends email for the password-reset flow. Whether email is
"set up" is decided by the configured mail backend: the development default is
the ``console`` backend (which prints to the terminal and never sends), so it
is considered *not* set up and the email-reset flow is hidden. Any explicitly
chosen backend (SMTP in production, locmem in tests) counts as set up.
"""

from django.conf import settings


def is_email_setup() -> bool:
    """Return True when a real sending mail backend is configured.

    Django 6.1 routes sending through the ``MAILERS`` setting, so the backend
    must be read from ``MAILERS["default"]["BACKEND"]``; the deprecated
    ``EMAIL_BACKEND`` setting is only a fallback when ``MAILERS`` is absent.
    """
    mailers = getattr(settings, "MAILERS", None)
    if mailers:
        backend = mailers.get("default", {}).get("BACKEND", "")
    else:
        backend = getattr(settings, "EMAIL_BACKEND", "")
    return backend != "django.core.mail.backends.console.EmailBackend"
