# Adopt Alpine.js and rewrite vanilla JS features it simplifies

- STATUS: OPEN
- PRIORITY: 75
- TAGS: frontend, javascript, alpine, refactor, feature

Adopt Alpine.js 3.15 (already vendored at static/libs/alpinejs) for interactive UI and rewrite existing vanilla JS features that Alpine genuinely simplifies. MUST be done only after the browser test layer task Task(20260808-115556) is implemented and green, so every rewrite is validated against the current behavior by the browser tests.

Prerequisite: Task(20260808-115556).

Scope:
- Load Alpine once in templates/services/base.html (and admin base templates where Alpine is used).
- Rewrite, one at a time, only the features where Alpine reduces complexity: login modal, mobile nav menu, custom-select widget, bookmark buttons, rating form, theme toggle state, and any other interactive component where Alpine is a clear win.
- Keep vanilla JS for features Alpine does not simplify (e.g. the OpenLayers admin map widget, scroll-progress logic) unless a rewrite clearly improves maintainability.
- Each rewrite must preserve exact current behavior and pass the browser tests; extend the browser test suite where coverage is missing.
- Remove obsolete vanilla JS files under static/services/js/ once their rewritten equivalents are covered by tests.
- Do not adopt Alpine for everything: use it only where it clearly simplifies the code.
- Update the README and any relevant docs to describe the JS architecture change.
