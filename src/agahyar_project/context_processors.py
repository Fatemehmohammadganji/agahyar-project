"""Template context processors for the Agahyar project."""

from django.conf import settings
from django.http import HttpRequest

from services.emailing import is_email_setup
from services.models import ThemePreference, get_site_contact_info


def matomo_context(request: HttpRequest) -> dict:
    """Add Matomo analytics settings to the template context.

    Returns MATOMO_URL, MATOMO_SITE_ID, and MATOMO_USER_ID from Django
    settings and the current request so that the base template can
    conditionally render the tracking snippet with user identification.
    """
    user_id = ""
    if getattr(request, "user", None) and request.user.is_authenticated:
        user_id = str(request.user.pk)
    return {
        "MATOMO_URL": getattr(settings, "MATOMO_URL", ""),
        "MATOMO_SITE_ID": getattr(settings, "MATOMO_SITE_ID", ""),
        "MATOMO_USER_ID": user_id,
    }


def user_theme_context(request: HttpRequest) -> dict:
    """Add the authenticated user's stored theme to the template context.

    Returns the theme name ("light" or "dark") as ``user_theme`` so the base
    template can render the initial ``data-theme`` attribute server-side as the
    no-JavaScript baseline. Anonymous users fall back to the default light
    theme, which the client-side script may still override via localStorage.
    """
    theme = "light"
    if getattr(request, "user", None) and request.user.is_authenticated:
        theme_pref = ThemePreference.objects.filter(user=request.user).first()
        if theme_pref is not None:
            theme = theme_pref.theme
    return {"user_theme": theme}


def contact_info_context(request: HttpRequest) -> dict:
    """Add the admin-editable contact details to the template context.

    Returns ``contact_email``, ``contact_phone`` and ``contact_working_hours``
    from the singleton :class:`SiteContactInfo` row (seeded from environment
    variables on first run) so the footer and contact page can render them on
    every page. Any value may be an empty string, in which case the templates
    hide it.
    """
    info = get_site_contact_info()
    return {
        "contact_email": info.email,
        "contact_phone": info.phone,
        "contact_working_hours": info.working_hours,
    }


def email_features_context(request: HttpRequest) -> dict:
    """Add email-based feature flags to the template context.

    Returns ``email_reset_enabled`` so templates can hide the email password
    reset flow when the admin has not configured a sending mail backend.
    """
    return {"email_reset_enabled": is_email_setup()}
