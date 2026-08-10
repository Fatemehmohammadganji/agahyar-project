# Store user theme preference in backend with non-JS fallback

- STATUS: CLOSED
- PRIORITY: 65
- TAGS: feature, ux, javascript

Currently the dark/light theme toggle only stores the choice in the browser
localStorage (static/services/js/main.js toggleTheme). The choice is lost when
switching devices/browsers, and users without JavaScript cannot switch the
theme at all because the toggle is a <button> with an onclick handler.

Requirements:

- Store the authenticated user's preferred theme (light/dark) in the backend
  so it follows them across devices.
- The theme toggle button must keep working for anonymous users via the
  existing localStorage mechanism.
- The toggle must have a no-JS fallback: it must be a link (anchor) to a
  dedicated toggle URL. When opened via GET:
  - Authenticated users: toggle the stored preference and redirect back to
    the page they came from.
  - Anonymous users: redirect to the login page with a next parameter that
    returns them to the originating page after login.
- When JavaScript is available and the user is logged in, the client sends the
  new preference to the server to persist it (via a POST request with CSRF
  protection), without a page reload.
- Guard against open-redirect vulnerabilities: any redirect target (next,
  referer) must be validated with url_has_allowed_host_and_scheme before use.

Design decisions:

- Use a new ThemePreference model (OneToOneField to User) instead of reusing
  UserProfile, because UserProfile requires a city and creating one implicitly
  would change existing user_city behavior.
- Expose the stored theme to templates via a context processor so the base
  template can render data-theme server-side as the no-JS baseline.

Scope:
- New ThemePreference model + migration + admin registration.
- New theme context processor registered in settings TEMPLATES.
- New theme_toggle_view (GET toggle + safe redirect, anonymous -> login;
  POST JSON sync, anonymous -> 401) + URL route.
- Convert the theme button in base.html to an anchor with the toggle URL and
  JS enhancement (onclick that preventDefaults and syncs when logged in).
- Update main.js toggleTheme to sync the preference to the server when the
  user is authenticated; keep anonymous behavior unchanged.
- Update README theme documentation.
- Add regression tests for the model, context processor, GET toggle with safe
  and unsafe redirect targets, anonymous redirect to login, POST sync, and the
  JavaScript behavior.
