# Improve admin panel UI/UX

- STATUS: OPEN
- PRIORITY: 50
- TAGS: ux, admin, design

Review and improve the overall user experience of the Django admin panel. This includes: adding better visual hierarchy and spacing, using consistent styling across all admin pages, adding helpful inline descriptions and help text for models and fields, improving the data transfer and stats pages with better visual feedback, adding breadcrumbs or navigation aids for deeper admin pages, ensuring all interactive elements have clear labels and states, and generally making the admin panel feel polished and professional for day-to-day staff use.
Some features could use dedicated pages that let staff manage the values with a better UI tailored to that specific thing (For example table view with a few columns does not work for contact messages at all; most pages would be better off showing cards instead of tables)

Also, ensure all the admin pages are under `ADMIN_URL` not any hardcoded prefix.
