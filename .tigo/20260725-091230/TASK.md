# Show OTP-requested-but-not-signed-up count on admin stats page

- STATUS: OPEN
- PRIORITY: 45
- TAGS: admin, analytics, feature

Add a new section or card to the admin stats page that displays the number of users who requested an OTP verification code but never completed the signup process. This metric helps identify drop-off in the registration funnel. The count should be derived from PhoneVerification records where an OTP was sent (e.g. created_at is set) but no corresponding UserProfile or User completion exists. Display the count prominently alongside existing stats, and optionally show the trend over time (e.g. weekly) similar to the existing charts on the stats page.
