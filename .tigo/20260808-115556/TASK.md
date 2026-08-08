# Add comprehensive browser tests for the frontend

- STATUS: OPEN
- PRIORITY: 90
- TAGS: testing, browser, frontend, quality

Set up a browser test layer for the interactive frontend and add comprehensive tests covering every existing feature. This is the mandatory prerequisite for the Alpine.js adoption task; every current behavior must be proven by a passing browser test before any JS rewrite is allowed.

Scope:
- Add Playwright for Python as a test dependency in pyproject.toml and uv.lock, and wire it into the Docker dev environment (docker-compose.dev.yml) and GitHub Actions CI on Python 3.12.
- Run the real Django application against the test database so pages render with the current templates, static files and vendored libraries.
- Cover the public pages (base template, search, service and center detail, blog list and detail, bookmarks) asserting they render without JavaScript errors, plus: theme toggle persistence, mobile nav, custom-select widget (search, load-more, keyboard and mouse selection), the anonymous bookmark-to-login modal flow, bookmark toggling for services and centers, rating submission, blog comment add and reply, admin tag list and blog image widgets, the admin OpenLayers map widget (render, marker placement, coordinate sync, coordinate search), and toast notifications.
- Keep tests deterministic: fixed seeded data, cleared localStorage, isolated sessions.
- Run the suite both locally in Docker and in CI.
