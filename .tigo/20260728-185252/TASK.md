# Image alt text for blog cover image

- STATUS: OPEN
- PRIORITY: 45
- TAGS: feature, blog, seo, a11y

Add an 'alt_text' CharField on BlogPost for the cover image alt attribute. Show it in the admin form. Use it in blog_detail.html as the <img alt> attribute of the cover image. Fall back to the post title if empty.
