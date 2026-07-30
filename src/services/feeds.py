"""RSS and Atom feeds for published blog posts."""

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from .models import BlogPost


class BlogRssFeed(Feed):
    """RSS 2.0 feed of the latest published blog posts.

    Served at ``/blog/feed/rss/``.  Returns the 20 most recent published
    posts with title, summary (or empty), author, keywords as categories,
    and publication date.

    .. note::

       Requires :setting:`SITE_URL` to be set in Django settings for
       generating absolute URLs.  Does **not** depend on
       ``django.contrib.sites``.
    """

    title = "آگاه\u200cیار - وبلاگ"
    description = "آخرین مطالب وبلاگ آگاه\u200cیار"

    def link(self) -> str:
        """Return the absolute URL of the blog list page."""
        return settings.SITE_URL + reverse("blog_list")

    def items(self):
        """Return the 20 most recent published posts."""
        return (
            BlogPost.objects.filter(is_published=True)
            .select_related("author")
            .defer("body")[:20]
        )

    def item_title(self, item: BlogPost) -> str:
        return item.title

    def item_description(self, item: BlogPost) -> str:
        return item.summary or ""

    def item_link(self, item: BlogPost) -> str:
        return settings.SITE_URL + reverse("blog_detail", kwargs={"slug": item.slug})

    def item_pubdate(self, item: BlogPost):
        return item.published_at

    def item_author_name(self, item: BlogPost) -> str:
        return item.author.get_full_name() or item.author.username

    def item_categories(self, item: BlogPost):
        if item.keywords:
            return [kw.strip() for kw in item.keywords.split(",")]
        return []


class BlogAtomFeed(BlogRssFeed):
    """Atom 1.0 feed of the latest published blog posts.

    Served at ``/blog/feed/atom/``.  Same data as :class:`BlogRssFeed`
    but in Atom 1.0 XML format.
    """

    feed_type = Atom1Feed
    subtitle = BlogRssFeed.description
