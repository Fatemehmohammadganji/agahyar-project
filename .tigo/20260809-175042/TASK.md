# Improve report dialog design and open login modal for anonymous users

- STATUS: CLOSED
- PRIORITY: 65
- TAGS: ux, frontend, javascript

The report dialog (templates/services/service_detail.html and
templates/services/center_detail.html) currently shows a custom anonymous
branch with ورود / ثبت‌نام buttons whose dimensions do not fit the dialog.
Improve the dialog design and route unauthenticated users to the shared login
modal (static/services/js/login-modal.js) instead of the custom prompt.

Scope:
- Remove the anonymous ورود / ثبت‌نام branch from the report dialog in both
  service_detail.html and center_detail.html.
- When an unauthenticated user clicks the report button, open the shared login
  modal instead of the report dialog (main.js openReportDialog).
- Handle HTTP 401 from the report API in main.js submitReport by opening the
  login modal (e.g. session expired mid-flow).
- Improve the report dialog design (spacing, header, dimensions, dark theme)
  and keep it consistent with the other native dialogs.
- Update existing tests and add regression tests for the new behavior.
