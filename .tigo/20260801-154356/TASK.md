# Make service search publicly accessible with a registration nudge

- STATUS: OPEN
- PRIORITY: 60
- TAGS: conversion, search

Remove the authentication gate from the search view in src/services/views.py so anonymous visitors can search services directly, and update its docstring accordingly. Adjust the test asserting anonymous access is a 302 redirect to instead assert a 200 response. Add a dismissible, non-intrusive registration CTA on templates/services/search.html suggesting signup benefits (save bookmarks, follow updates), preserving the next parameter. Add tests for anonymous search access and the nudge display/dismissal.
