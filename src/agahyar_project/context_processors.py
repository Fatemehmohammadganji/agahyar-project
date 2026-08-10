"""Template context processors for the Agahyar project."""

from django.conf import settings
from django.http import HttpRequest

from services.models import ThemePreference


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
