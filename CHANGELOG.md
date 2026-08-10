# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [1.8.0] - 2026-08-11

### Added

- **Email-based password reset flow**: Custom views that 404 and hide all
  frontend links until a real sending mail backend is configured
  (`is_email_setup()`), a per-IP rate limit (`5/m`) on the reset form, a
  branded RTL HTML email with a reset button plus Persian subject and
  plain-text fallback, and a configurable `PASSWORD_RESET_TIMEOUT`.
  The confirm page renders a friendly invalid-link state for expired/invalid
  tokens instead of crashing.
- **Theme preference persistence**: The no-JS theme toggle now stores the
  user's light/dark choice in the backend and restores it on every page.
- **Admin-editable contact info**: A singleton `SiteContactInfo` model lets
  admins edit the site's email, phone, and working hours from the admin panel;
  each field is hidden on the frontend when empty.
- **Service center bookmarks**: Centers can be bookmarked, listed on the
  bookmarks page, and enforce exactly-one-target with a DB check constraint.
  Bookmark buttons are shown to anonymous users and open the shared login
  modal, then set the bookmark state after login.
- **Public service search with signup nudge**: Search is accessible to
  anonymous visitors, with a registration prompt for full results.
- **Shared native-dialog login modal**: A single accessible login modal
  (native `<dialog>`) reused across service, center, and blog pages; the
  `next` destination is honored after login.
- **Anonymous comment reactions**: Visitors can like/dislike comments via the
  login modal, with 403 session-expiry handling.
- **FAQ cache invalidation**: The FAQ cache is invalidated when FAQs are
  edited (keyed on `max updated_at`).

### Changed

- **Django 6.1 required**: `django>=6.1.0`; email configuration now uses the
  `MAILERS` setting (the deprecated `EMAIL_BACKEND` family is removed as the
  source of truth).
- **Bookmark toggle replaced by set-state**: The bookmark buttons set an
  explicit state instead of toggling, so the UI and server stay in sync.
- Dependency upgrades, vendored library refreshes, and lint fixes.

### Fixed

- **Theme toggle hardening**: Unsupported HTTP methods are rejected with 405
  (previously they fell through to the toggle logic and changed the theme);
  valid JSON that is not an object (`[]`, `null`) now returns 400 instead of
  crashing with a 500.
- **Email reset gating**: A missing/empty mail backend is treated as not set
  up, and the per-IP rate limit no longer fires (403) when the feature is
  disabled, so disabled email consistently returns 404.
- **Bookmark/rating request validation**: Bookmark and rating handlers require
  a JSON object body; `rate_center` is restricted to POST.
- **Login/rating UI**: Login redirects honor the requested `next` destination;
  native dialogs close only on backdrop click; the CSRF token is rotated on
  all matching inputs after login; star ratings support keyboard selection.

## [1.7.0] - 2026-07-30

### Added

- **Blog system with CKEditor 5**: Full-featured blog including post creation,
  editing, publishing with WYSIWYG editor (Decoupled Document build v44.3.0),
  Persian UI, inline image upload, and admin media manager.
- **Blog admin CRUD**: Custom admin pages with card-based UI, drag-and-drop
  image upload widget, toggle checkbox widget, Persian labels, tag input with
  autocomplete, and slug auto-generation.
- **Blog frontend UI/UX**: Card-based list with hover effects, reading time
  badge, scroll progress bar, table of contents, image lightbox, author bio,
  related posts, keyword pills, star ratings, and accessible login modal.
- **RSS/Atom feeds**: Blog feeds at `/blog/feed/rss/` and `/blog/feed/atom/`
  with autodiscovery link tags.
- **Blog search**: Search by title, summary, and keywords with result header
  and separate empty states.
- **Blog preview URL**: Staff-only preview endpoint at `/blog/<slug>/preview/`.
- **Rich-text normalization**: `plaintext` template filter that inserts spaces
  around block-level HTML elements before stripping tags.
- **Accessibility improvements**: Login form now has `id`/`for` attributes,
  `aria-invalid`, and `aria-describedby` on username and password fields.
- **Admin card-based pages with AJAX actions**: New admin dashboard and
  management pages for data transfer (export/import), bookmarks, and user
  management with inline AJAX delete and search.

### Changed

- OTP abandonment stats now correctly exclude verified phone numbers.

### Fixed

- Matomo duplicate `setTrackerUrl`/`setSiteId` calls removed.
- Collapsed content overflow in the profile page was fixed.
- h1 logo replaced with span elements for SEO.
- Space variant of brand name added to meta keywords for SEO.

## [1.6.2] - 2026-07-24

### Added

- Matomo user ID tracking for authenticated users.
- Center names on nearby centers page link to the center detail page.
- Map icon buttons with `fa-map-location-dot` replace text buttons.

### Changed

- Nearby centers page redesigned with tighter card layout.
- All user-visible numbers (center names, postal codes, phone numbers,
  OTP countdown timers, titles, and meta tags) now display in Persian
  digits (`۰۱۲۳۴۵۶۷۸۹`).

## [1.6.1] - 2026-07-23

### Fixed

- Removed Leaflet OpenStreetMap attribution text from maps
- Fixed maps not loading on page load (ReferenceError from `toPersianDigits` called before `main.js` defer script executed)
- Removed unnecessary `matomo-network` to fix intermittent 504 Gateway Timeout on Matomo dashboard
- Added `*.DOMAIN` to CSP `script-src` directive to allow Matomo analytics

## [1.6.0] - 2026-07-22

### Added

- **Comment reactions**: Like/dislike buttons on comments for both services
  and service centers. A new `CommentReaction` model tracks user reactions
  with unique constraints. The API exposes a `/react/` endpoint; the
  frontend updates counts in-place and highlights the user's active
  reaction.
- **Self-hosted Matomo analytics**: Added `docker-compose.matomo.yml` with
  Matomo 5 and MySQL 8.0 behind Traefik. Tracking snippet in `base.html`
  is conditionally rendered when `MATOMO_URL` and `MATOMO_SITE_ID` are set.
  A context processor supplies the values to templates.
- **Service description field**: New optional `description` TextField on the
  `Service` model. Rendered on the service detail page between the header
  and documents sections, hidden when empty. Supports multi-paragraph text.
- **Per-phone SMS rate limiting**: Cache-based limiter in `sms.py` blocks
  SMS sends to a single phone number after 5 messages per 10-minute window.
  Enforced inside `SMSClient.send_otp()` so all SMS paths are protected.
  The `resend_otp_api` and `resend_profile_otp_api` views now use
  `block=True` on the `@ratelimit` decorator.

### Changed

- **Service detail page hides empty fields**: Cost, duration, documents,
  and steps sections are now wrapped in `{% if %}` guards and are not
  rendered when the field is empty.
- **Pagination redesign**: Replaced prev/next-only pagination with numbered
  page buttons, ellipsis for distant pages, and a styled active-page
  indicator. Both `service_list.html` and `search.html` use semantic
  `<nav>` elements with `aria-label`.
- **Comment full name**: Comments now display the user's full name
  (first + last) instead of just the first name.
- **Alert replaced with toast notifications**: The native `alert()` call in
  the reaction error handler is replaced with a slide-up toast component
  (`showToast`). The existing `showReportSuccess` function now uses the
  same generic toast.
- **JS Unicode escapes decoded**: All escaped Persian/Arabic text in
  JavaScript files is now readable UTF-8. A garbled message in the
  geolocation error handler was corrected.
- **Admin data transfer import hardened**: Upload files larger than 10 MB
  or containing more than 10,000 records are rejected before reading into
  memory. `DATA_UPLOAD_MAX_MEMORY_SIZE` is set to 10 MB in settings.
- **Admin stats cached**: The admin dashboard view now caches aggregate
  queries for 5 minutes to avoid repeated full-table scans.
- **Sitemap memory-efficient**: Service and center querysets in the sitemap
  view now use `.iterator()` to avoid loading all objects into memory.
- **Comment reaction aggregation optimized**: The reaction counting loop
  in `service_detail` and `center_detail` now iterates through the prefetch
  cache once per comment instead of calling `.reactions.all()` three times.

### Fixed

- **Duplicate reaction requests on center detail page**: Removed a duplicate
  `main.js` include in `center_detail.html` that caused the delegated
  reaction click handler to fire twice, toggling the reaction back off.
- **SEO page titles**: Removed duplicated brand name from page titles.
  Base template now provides the default `<title>` with child templates
  supplying only the page-specific part.
- **Secrets management**: `SECRET_KEY` is required when `DEBUG=False`.
  System checks (`security.W001`/`W002`) validate security headers in
  production. Profiling middleware is gated on `DEBUG=True` and restricted
  to staff.
- **Access control**: `/users/` endpoint restricted to staff. API
  schema/docs views restricted to staff. Default DRF permission changed to
  `IsAuthenticated`. `PhoneVerification` removed from exportable models.
  Open redirect in password reset fixed with `|urlencode`.
- **Comment reaction frontend**: JS now checks `response.ok` before
  updating the UI. Reaction buttons on own comments are disabled in the
  template.

## [1.5.1] - 2026-07-22

### Fixed

- **Duplicate bookmark requests on service detail page**: Removed a duplicate
  `main.js` load in `service_detail.html` that caused the delegated bookmark
  click handler to fire twice per click, undoing the toggle.
- **OTP expiry tests**: Increased backdate from 10 to 30 minutes to match
  the new 20-minute `OTP_EXPIRE_MINUTES`.

## [1.5.0] - 2026-07-21

### Added

- **AJAX bookmark toggle**: Bookmark/unbookmark buttons on the home, services,
  search, dashboard, bookmarks, and service detail pages now use a delegated
  click handler that sends a POST via `fetch` in the background. The page no
  longer reloads when toggling a bookmark. On the bookmarks page, the card
  fades out and is removed from the DOM.
- **Tag list widget for admin**: A new `TagListWidget` for managing
  pipe/comma-separated list fields (documents, steps, keywords) in the admin
  panel. Supports add, remove, and drag-and-drop reorder with per-field
  configurable separator.
- **OTP security hardening**: Per-OTP brute-force counter
  (`PhoneVerification.failed_attempts`) blocks after 5 wrong attempts with an
  `otp/max-attempts` error. OTP expiry increased from 5 to 20 minutes
  (env-overridable via `OTP_EXPIRE_MINUTES`). Pending registration token TTL
  increased from 5 to 60 minutes. Session cookie age increased from 1 hour to
  6 hours.
- **OTP SMS delivery notice**: All OTP pages now advise users to wait up to 5
  minutes for SMS delivery due to potential carrier delays.

## [1.4.0] - 2026-07-21

### Added

- **City selector with search and lazy loading**: A searchable city dropdown
  backed by a new `/api/cities/` endpoint. Cities are ranked by service center
  count (top 20 shown by default), with AJAX search and infinite scroll for
  additional results. The `RegisterForm` and `ProfileForm` validate that the
  submitted city exists in the database.
- **Admin bulk data export/import**: A new admin page at `admin/data-transfer/`
  for exporting and importing all project data (services, centers, ratings,
  comments, etc.) as JSON. Supports dry-run mode, foreign key ordering, and
  M2M relationship handling. `ServiceCenterResource` now exports M2M services;
  a new `ServiceCenterPhoneResource` is available for phone number data.
- **Favicon with rounded hexagon design**: Added a custom favicon (teal
  `#1a5f7a` rounded hexagon with Persian letter "Alef") for the main site and
  a darker variant (`#0f3d52`) for the admin panel. A reusable generator
  script is at `scripts/generate_favicons.py`.
- **GitHub repository link**: Footer and about page now link to the GitHub
  repository with a Font Awesome icon.

### Changed

- **City dropdown overflows collapsible sections**: Changed `.collapsible-content`
  from `overflow: hidden` to `overflow: visible` so that the city selector
  dropdown can extend beyond the collapsed edit section.
- **Favicon generator is cross-platform**: The font path in
  `scripts/generate_favicons.py` now searches multiple OS-specific locations
  instead of hardcoding a Windows path. Pillow is declared as an optional
  dependency under `[project.optional-dependencies].scripts`.

### Fixed

- **OTP/registration test suite**: Added an `ensure_test_cities` pytest fixture
  that creates `ServiceCenter` records for cities used in tests. This fixes 28
  pre-existing test failures caused by `clean_city()` rejecting cities not
  present in the database.

## [1.3.0] - 2026-07-19

### Added

- **Login via phone number or email**: Users can now log in with their
  username, phone number, or email address. A custom authentication backend
  resolves the identifier across all three fields.
- **Username validation**: Registration now rejects all-numeric usernames and
  usernames containing the `@` character.
- **Service centers provide multiple services**: The `ServiceCenter.service`
  foreign key has been replaced with a `services` many-to-many field, allowing
  a single center to offer multiple government services.
- **Mailcow email integration**: Added `docker-compose.mailcow.yml` for
  self-hosted email via Mailcow (Postfix/Dovecot/Rspamd). Email settings in
  `settings.py` are now fully environment-driven. Created `MAIL_SETUP.md`
  with complete setup, DNS, and troubleshooting instructions.

### Changed

- **Email settings are environment-driven**: `EMAIL_BACKEND`, `EMAIL_HOST`,
  `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`,
  `DEFAULT_FROM_EMAIL`, and `SERVER_EMAIL` are now configurable via
  environment variables. The console backend remains the default for
  development.
- **Admin center list**: Shows comma-separated service names instead of a
  single service, with `filter_horizontal` widget for M2M editing.
- **API center serializer**: Exposes `service_names` (list) instead of
  `service_name` (single string).
- **Center detail page**: Displays all services a center provides with links,
  instead of a single service.
- **Login template**: Label and placeholder updated to indicate phone and
  email login support.

## [1.2.0] - 2026-07-18

### Changed

- **City-based center ordering**: The service detail page now orders
  centers with the user's profile city first (defaulting to Tehran for
  anonymous users), showing all centers available via "load more" instead
  of filtering to only the user's city.
- **Map syncs with loaded centers**: The service detail map now shows
  markers only for centers loaded in the list, adding markers as new
  pages are loaded via AJAX.

### Fixed

- **City name validation**: Cleaned up invalid city names in the SRA
  epishkhan data pipeline (street names, address fragments, province
  names no longer used as city names).

## [1.1.0] - 2026-07-18

### Added

- **Admin map widget with Neshan search**: The admin map widget now includes
  a search box powered by the Neshan API. Admins can search for locations and
  click to set latitude/longitude coordinates directly on the widget, with
  automatic sync between the map and coordinate inputs.
- **Multiple phone numbers per service center**: A new `ServiceCenterPhone`
  model allows each service center to have multiple phone numbers with labels
  (main, fax, mobile, other) and ordering. Phone numbers are displayed as
  clickable `tel:` links on the frontend using Persian digits.

### Fixed

- **CLI commands now use English**: The `LANGUAGE_CODE` has been changed from
  `fa` to `en-us`, with `LocaleMiddleware` added so that web requests still
  receive Persian via the browser's `Accept-Language` header. This ensures
  management commands like `createsuperuser` display English prompts and
  messages.
- **Docker Compose certResolver labels**: Added missing certResolver labels to
  the production Docker Compose configuration.
- **Test fix for Neshan search mock**: Added missing `close()` method to the
  mock `FP` object in the Neshan search proxy test to prevent
  `PytestUnraisableExceptionWarning`.
