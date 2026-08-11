# Blog post view counter

- STATUS: CLOSED
- PRIORITY: 35
- TAGS: feature, blog

Add a PositiveIntegerField 'view_count' with default=0 to BlogPost. Increment on each blog_detail GET (excluding staff previews). Display the count on blog_list and blog_detail as 'X بازدید'.
