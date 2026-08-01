# Reuse login modal on service and center detail pages for rating and commenting

- STATUS: OPEN
- PRIORITY: 80
- TAGS: conversion, ui/ux, login

Replace the full-page login redirect links in the login-prompt blocks of templates/services/service_detail.html and templates/services/center_detail.html with buttons that open the shared login modal. For anonymous users, intercept star-rating clicks on the center rating widget so the modal opens instead of submitting. When the modal login succeeds, perform the pending action (send the rating/comment) immediately and only then do a full page reload so the server renders the authenticated state.
