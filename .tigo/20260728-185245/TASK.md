# RSS/Atom feed for blog

- STATUS: OPEN
- PRIORITY: 50
- TAGS: feature, blog, rss

Add RSS and Atom feeds for published blog posts using Django's syndication framework. Create a Feed subclass in feeds.py, wire it in urls.py, and add autodiscovery <link> tags in the blog_list template head.
