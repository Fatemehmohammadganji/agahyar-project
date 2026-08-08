# Show bookmark buttons to unauthenticated users and open the login modal on click

- STATUS: CLOSED
- PRIORITY: 75
- TAGS: conversion, bookmark, login

Remove the is_authenticated template gates around the bookmark buttons in templates/services/service_list.html, templates/services/home.html and templates/services/service_detail.html so anonymous users see them rendered with data-bookmarked=false. Intercept anonymous bookmark clicks in the shared JS and open the login modal instead of issuing the POST. Replace the 401 window.location.href=/auth/login/ redirects in static/services/js/main.js (bookmark toggle and comment reactions) with the shared modal. After successful modal login, perform the pending bookmark toggle and then reload the page.
