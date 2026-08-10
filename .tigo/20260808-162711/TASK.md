# Make bookmark endpoints set a desired state instead of toggling

- STATUS: CLOSED
- PRIORITY: 75
- TAGS: bookmark, api, bugfix, desync

Fix the bookmark desync bug: the user clicks a bookmark button while logged out, then logs in
via the shared modal, and the frontend POSTs to `/bookmark/<id>/` which TOGGLES the state. If the
service was already bookmarked before logout, the toggle unbookmarks it - the opposite of what the
user wanted.

Change the bookmark API so the server receives the desired state (bookmark vs unbookmark) instead
of toggling. The endpoints `/bookmark/<service_id>/` and `/bookmark/center/<center_id>/` must
parse a `bookmarked` boolean from the request (JSON body for AJAX, form field for regular POST) and
set the state idempotently (create when true, delete when false). The frontend must always send the
desired state. This also fixes other desyncs (e.g. multiple open tabs).
