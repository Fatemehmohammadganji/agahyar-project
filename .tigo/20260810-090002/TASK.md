# Make contact email and phone customizable by admins

- STATUS: CLOSED
- PRIORITY: 60
- TAGS: feature, admin, ux

The contact email and phone number shown on the frontend (footer in
templates/services/base.html and the اطلاعات تماس block in
templates/services/contact.html) are hardcoded. Admins must be able to change
them without touching the code.

Requirements:

- Store the contact email, phone and working hours in the database in a
  single-instance settings model so admins can edit them from the Django
  admin panel.
- On first run, seed the database row from environment variables
  (CONTACT_EMAIL / CONTACT_PHONE / CONTACT_WORKING_HOURS); afterwards the
  database is the source of truth and admins change it in the admin panel.
- All three values may be empty. When empty, the corresponding field must be
  hidden across all frontend pages (footer and contact page); when both
  email and phone are empty, the footer contact section must not render.
- Provide a good user experience: clickable mailto: and tel: links, correct
  handling of Persian digits in phone numbers, an admin panel that cannot
  accidentally create a second row, and a polished contact-info block on the
  contact page (icon items for email, phone and working hours).
- Add regression tests for seeding, hiding empty fields, and admin behavior.

Design decisions:

- SiteContactInfo singleton model (pk=1) with email, phone and working_hours
  CharFields that allow blank values.
- A context processor exposes contact_email, contact_phone and
  contact_working_hours to every template so the footer works on all pages
  without changing every view.
- get_site_contact_info() helper seeds the row from settings on first access.
