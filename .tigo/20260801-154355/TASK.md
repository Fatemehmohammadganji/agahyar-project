# Add bookmarking support for service centers

- STATUS: OPEN
- PRIORITY: 70
- TAGS: ux, bookmark, feature

Extend the Bookmark model so service centers can also be bookmarked (new FK/migration), update admin, update the bookmarks list page, and add a bookmark button to templates/services/center_detail.html visible to anonymous users as well. Reuse the shared login modal flow when an anonymous user clicks it, perform the toggle after successful login, then reload. Add tests covering center bookmark toggle, listing, duplicate handling, and the anonymous flow.
