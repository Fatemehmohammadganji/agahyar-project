# Extract shared login modal into a reusable partial and global JS

- STATUS: OPEN
- PRIORITY: 80
- TAGS: ui/ux, login, refactor

Extract the login modal markup from templates/services/blog_detail.html into templates/services/partials/login_modal.html and include it in the base layout so every page has it. Move the modal logic (open/close, focus trap, Escape, backdrop click, AJAX login POST to /login/) from static/services/js/blog-detail.js into a new static/services/js/login-modal.js loaded globally. Make the modal prompt text configurable per trigger via a data attribute and expose an onLogin continuation hook so callers can run a follow-up action (e.g. submit a rating) before the full page reload.
