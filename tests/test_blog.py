"""Tests for the BlogPost and BlogPostRating models, views, and admin."""

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from services.models import BlogPost, BlogPostRating, UserProfile


@pytest.mark.django_db
class TestBlogPostModel:
    def test_str_returns_title(self):
        post = BlogPost.objects.create(
            title="مطلب آزمایشی",
            author=User.objects.create_user(username="author1"),
        )
        assert str(post) == "مطلب آزمایشی"

    def test_save_auto_generates_slug_on_creation(self):
        post = BlogPost.objects.create(
            title="مطلب آزمایشی",
            author=User.objects.create_user(username="author1"),
        )
        assert post.slug == "مطلب-آزمایشی"

    def test_save_sets_published_at_when_published(self):
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
            is_published=True,
        )
        assert post.published_at is not None

    def test_save_does_not_change_published_at_on_subsequent_saves(self):
        author = User.objects.create_user(username="author1")
        post = BlogPost.objects.create(
            title="test",
            author=author,
            is_published=True,
        )
        original = post.published_at
        post.title = "updated"
        post.save()
        assert post.published_at == original

    def test_display_image_url_prefers_image_url_over_image(self):
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
            image_url="https://example.com/img.jpg",
        )
        assert post.display_image_url == "https://example.com/img.jpg"

    def test_display_image_url_returns_none_when_no_image(self):
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
        )
        assert post.display_image_url is None

    def test_get_keywords_list_returns_empty_when_no_keywords(self):
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
        )
        assert post.get_keywords_list() == []

    def test_get_keywords_list_splits_by_comma(self):
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
            keywords="آموزش, روانشناسی, سلامت",
        )
        assert post.get_keywords_list() == ["آموزش", "روانشناسی", "سلامت"]

    def test_get_keywords_list_strips_whitespace(self):
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
            keywords="  آموزش , روانشناسی ",
        )
        assert post.get_keywords_list() == ["آموزش", "روانشناسی"]

    def test_keywords_appear_in_detail_page(self):
        author = User.objects.create_user(username="author1")
        post = BlogPost.objects.create(
            title="test",
            author=author,
            keywords="آموزش, سلامت",
            is_published=True,
        )
        client = Client()
        client.force_login(author)
        response = client.get(reverse("blog_detail", kwargs={"slug": post.slug}))
        assert response.status_code == 200
        assert "آموزش" in response.content.decode()
        assert "سلامت" in response.content.decode()

    def test_alt_text_defaults_to_empty_string(self):
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
        )
        assert post.alt_text == ""

    def test_alt_text_fallback_to_title_in_detail_image(self):
        author = User.objects.create_user(username="author1")
        post = BlogPost.objects.create(
            title="عنوان پست",
            author=author,
            image_url="https://example.com/img.jpg",
            is_published=True,
        )
        client = Client()
        response = client.get(reverse("blog_detail", kwargs={"slug": post.slug}))
        html = response.content.decode()
        assert 'alt="عنوان پست"' in html

    def test_alt_text_used_when_set_in_detail_image(self):
        author = User.objects.create_user(username="author1")
        post = BlogPost.objects.create(
            title="عنوان پست",
            alt_text="توضیح تصویر",
            author=author,
            image_url="https://example.com/img.jpg",
            is_published=True,
        )
        client = Client()
        response = client.get(reverse("blog_detail", kwargs={"slug": post.slug}))
        html = response.content.decode()
        assert 'alt="توضیح تصویر"' in html
        assert 'alt="عنوان پست"' not in html

    def test_alt_text_used_in_list_when_set(self):
        author = User.objects.create_user(username="author1")
        BlogPost.objects.create(
            title="عنوان پست",
            alt_text="توضیح تصویر",
            author=author,
            image_url="https://example.com/img.jpg",
            is_published=True,
        )
        client = Client()
        response = client.get(reverse("blog_list"))
        html = response.content.decode()
        assert 'alt="توضیح تصویر"' in html

    def test_userprofile_bio_field_exists(self, client):
        user = User.objects.create_user(username="author1")
        profile = UserProfile.objects.create(user=user, city="تهران")
        assert profile.bio == ""
        profile.bio = "نویسنده و محتواگذار"
        profile.save()
        db_profile = UserProfile.objects.get(pk=profile.pk)
        assert db_profile.bio == "نویسنده و محتواگذار"

    def test_blog_detail_shows_author_bio_when_set(self, client):
        author = User.objects.create_user(
            username="author1",
            first_name="علی",
            last_name="کریمی",
        )
        UserProfile.objects.create(
            user=author, city="تهران", bio="نویسنده محتوای آموزشی"
        )
        post = BlogPost.objects.create(
            title="test",
            author=author,
            is_published=True,
        )
        response = client.get(f"/blog/{post.slug}/")
        html = response.content.decode()
        assert "علی کریمی" in html
        assert "نویسنده محتوای آموزشی" in html

    def test_blog_detail_author_bio_omitted_when_empty(self, client):
        author = User.objects.create_user(username="author1")
        UserProfile.objects.create(user=author, city="تهران")
        post = BlogPost.objects.create(
            title="test",
            author=author,
            is_published=True,
        )
        response = client.get(f"/blog/{post.slug}/")
        html = response.content.decode()
        assert "author1" in html


@pytest.mark.django_db
class TestBlogPostRatingModel:
    def test_str_representation(self):
        user = User.objects.create_user(username="testuser")
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
        )
        rating = BlogPostRating.objects.create(user=user, blog_post=post, score=4)
        assert str(rating) == "testuser - test - 4"

    def test_unique_together_user_post(self):
        user = User.objects.create_user(username="testuser")
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
        )
        BlogPostRating.objects.create(user=user, blog_post=post, score=3)
        with pytest.raises(Exception):
            BlogPostRating.objects.create(user=user, blog_post=post, score=5)


@pytest.mark.django_db
class TestBlogViews:
    def test_blog_list_returns_200(self, client):
        response = client.get("/blog/")
        assert response.status_code == 200

    def test_blog_list_shows_only_published_posts(self, client):
        author = User.objects.create_user(username="author1")
        BlogPost.objects.create(
            title="published",
            author=author,
            is_published=True,
        )
        BlogPost.objects.create(
            title="draft",
            author=author,
            is_published=False,
        )
        response = client.get("/blog/")
        assert response.status_code == 200
        assert "published" in response.content.decode()
        assert "draft" not in response.content.decode()

    def test_blog_detail_returns_200_for_published(self, client):
        author = User.objects.create_user(username="author1")
        post = BlogPost.objects.create(
            title="test",
            author=author,
            is_published=True,
        )
        response = client.get(f"/blog/{post.slug}/")
        assert response.status_code == 200

    def test_blog_detail_returns_404_for_draft(self, client):
        author = User.objects.create_user(username="author1")
        post = BlogPost.objects.create(
            title="test",
            author=author,
            is_published=False,
        )
        response = client.get(f"/blog/{post.slug}/")
        assert response.status_code == 404

    def test_blog_detail_returns_404_for_nonexistent_slug(self, client):
        response = client.get("/blog/nonexistent-slug/")
        assert response.status_code == 404

    def test_related_posts_shown_when_keywords_match(self, client):
        author = User.objects.create_user(username="author1")
        post = BlogPost.objects.create(
            title="main",
            keywords="آموزش, سلامت",
            author=author,
            is_published=True,
        )
        BlogPost.objects.create(
            title="related one",
            keywords="آموزش",
            author=author,
            is_published=True,
        )
        BlogPost.objects.create(
            title="related two",
            keywords="سلامت",
            author=author,
            is_published=True,
        )
        BlogPost.objects.create(
            title="unrelated",
            keywords="فناوری",
            author=author,
            is_published=True,
        )
        response = client.get(f"/blog/{post.slug}/")
        html = response.content.decode()
        assert "related one" in html
        assert "related two" in html
        assert "unrelated" not in html
        assert "مطالب مرتبط" in html

    def test_related_posts_hidden_when_no_keywords(self, client):
        author = User.objects.create_user(username="author1")
        post = BlogPost.objects.create(
            title="main",
            author=author,
            is_published=True,
        )
        response = client.get(f"/blog/{post.slug}/")
        assert "مطالب مرتبط" not in response.content.decode()

    def test_related_posts_hidden_when_only_self_matches(self, client):
        author = User.objects.create_user(username="author1")
        post = BlogPost.objects.create(
            title="main",
            keywords="آموزش",
            author=author,
            is_published=True,
        )
        BlogPost.objects.create(
            title="other",
            keywords="فناوری",
            author=author,
            is_published=True,
        )
        response = client.get(f"/blog/{post.slug}/")
        assert "مطالب مرتبط" not in response.content.decode()

    def test_blog_list_search_by_title(self, client):
        author = User.objects.create_user(username="author1")
        BlogPost.objects.create(
            title="آموزش ری اکت",
            author=author,
            is_published=True,
        )
        BlogPost.objects.create(
            title="آموزش پایتون",
            author=author,
            is_published=True,
        )
        response = client.get("/blog/?q=ری اکت")
        assert response.status_code == 200
        html = response.content.decode()
        assert "آموزش ری اکت" in html
        assert "آموزش پایتون" not in html

    def test_blog_list_search_by_summary(self, client):
        author = User.objects.create_user(username="author1")
        BlogPost.objects.create(
            title="post one",
            summary="مربوط به سلامت",
            author=author,
            is_published=True,
        )
        BlogPost.objects.create(
            title="post two",
            summary="مربوط به آموزش",
            author=author,
            is_published=True,
        )
        response = client.get("/blog/?q=سلامت")
        assert response.status_code == 200
        assert "post one" in response.content.decode()
        assert "post two" not in response.content.decode()

    def test_blog_list_search_shows_result_header(self, client):
        author = User.objects.create_user(username="author1")
        BlogPost.objects.create(
            title="test",
            author=author,
            is_published=True,
        )
        response = client.get("/blog/?q=test")
        html = response.content.decode()
        assert "نتیجه جستجو برای" in html
        assert "test" in html

    def test_blog_list_search_no_results_shows_empty_state(self, client):
        response = client.get("/blog/?q=xyznotfound")
        html = response.content.decode()
        assert "نتیجه‌ای یافت نشد" in html


ADMIN_PREFIX = "admin/"


def _staff_client() -> Client:
    c = Client()
    User.objects.create_superuser(username="admin", password="admin", email="")
    c.login(username="admin", password="admin")
    return c


@pytest.mark.django_db
class TestBlogAdmin:
    def test_staff_can_see_blog_admin(self, admin_client):
        response = admin_client.get("/admin/services/blogpost/")
        assert response.status_code == 200

    def test_non_staff_cannot_see_blog_admin(self, client):
        response = client.get("/admin/services/blogpost/")
        assert response.status_code in (302, 403)


@pytest.mark.django_db
class TestCustomBlogAdmin:
    def test_list_requires_staff(self, client):
        response = client.get(f"/{ADMIN_PREFIX}blog/")
        assert response.status_code in (302, 403)

    def test_list_returns_200_for_staff(self):
        staff = _staff_client()
        response = staff.get(f"/{ADMIN_PREFIX}blog/")
        assert response.status_code == 200

    def test_create_get_requires_staff(self, client):
        response = client.get(f"/{ADMIN_PREFIX}blog/create/")
        assert response.status_code in (302, 403)

    def test_create_get_returns_200_for_staff(self):
        staff = _staff_client()
        response = staff.get(f"/{ADMIN_PREFIX}blog/create/")
        assert response.status_code == 200

    def test_create_post_creates_post(self):
        staff = _staff_client()
        data = {
            "title": "پست جدید",
            "slug": "پست-جدید",
            "summary": "خلاصه",
            "body": "<p>متن</p>",
            "is_published": True,
        }
        response = staff.post(f"/{ADMIN_PREFIX}blog/create/", data, follow=True)
        assert response.status_code == 200
        assert BlogPost.objects.filter(title="پست جدید").exists()

    def test_create_post_without_staff_denied(self, client):
        data = {
            "title": "پست جدید",
            "slug": "پست-جدید",
            "body": "<p>متن</p>",
        }
        response = client.post(f"/{ADMIN_PREFIX}blog/create/", data)
        assert response.status_code in (302, 403)
        assert not BlogPost.objects.filter(title="پست جدید").exists()

    def test_create_redirects_after_success(self):
        staff = _staff_client()
        data = {
            "title": "پست جدید",
            "slug": "پست-جدید",
            "summary": "خلاصه",
            "body": "<p>متن</p>",
        }
        response = staff.post(f"/{ADMIN_PREFIX}blog/create/", data)
        assert response.status_code == 302
        assert response.url == f"/{ADMIN_PREFIX}blog/"

    def test_edit_get_requires_staff(self, client):
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="a"),
        )
        response = client.get(f"/{ADMIN_PREFIX}blog/{post.id}/edit/")
        assert response.status_code in (302, 403)

    def test_edit_get_returns_200_for_staff(self):
        staff = _staff_client()
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="a"),
        )
        response = staff.get(f"/{ADMIN_PREFIX}blog/{post.id}/edit/")
        assert response.status_code == 200

    def test_edit_post_updates_post(self):
        staff = _staff_client()
        author = User.objects.create_user(username="a")
        post = BlogPost.objects.create(title="old", author=author)
        data = {
            "title": "updated",
            "slug": post.slug,
            "summary": "new summary",
            "body": "<p>new body</p>",
        }
        staff.post(f"/{ADMIN_PREFIX}blog/{post.id}/edit/", data)
        post.refresh_from_db()
        assert post.title == "updated"
        assert post.summary == "new summary"

    def test_delete_requires_staff(self, client):
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="a"),
        )
        response = client.post(f"/{ADMIN_PREFIX}blog/{post.id}/delete/")
        assert response.status_code in (302, 403)
        assert BlogPost.objects.filter(id=post.id).exists()

    def test_delete_removes_post(self):
        staff = _staff_client()
        author = User.objects.create_user(username="a")
        post = BlogPost.objects.create(title="to-delete", author=author)
        staff.post(f"/{ADMIN_PREFIX}blog/{post.id}/delete/")
        assert not BlogPost.objects.filter(id=post.id).exists()

    def test_delete_get_method_returns_405(self):
        staff = _staff_client()
        author = User.objects.create_user(username="a")
        post = BlogPost.objects.create(title="test", author=author)
        response = staff.get(f"/{ADMIN_PREFIX}blog/{post.id}/delete/")
        assert response.status_code == 405

    def test_edit_nonexistent_returns_404(self):
        staff = _staff_client()
        response = staff.get(f"/{ADMIN_PREFIX}blog/99999/edit/")
        assert response.status_code == 404

    def test_delete_nonexistent_returns_404(self):
        staff = _staff_client()
        response = staff.post(f"/{ADMIN_PREFIX}blog/99999/delete/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestBlogRatingAPI:
    def test_rating_requires_login(self, client):
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
            is_published=True,
        )
        response = client.post(
            f"/api/rate-blog-post/{post.id}/",
            {"score": 4},
            content_type="application/json",
        )
        assert response.status_code == 401

    def test_rate_and_get_average(self, client):
        User.objects.create_user(username="testuser", password="pass")
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
            is_published=True,
        )
        client.login(username="testuser", password="pass")
        response = client.post(
            f"/api/rate-blog-post/{post.id}/",
            {"score": 4},
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_score"] == 4
        assert data["count"] == 1
        assert data["average"] == 4.0

    def test_score_out_of_range_rejected(self, client):
        User.objects.create_user(username="testuser", password="pass")
        post = BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
            is_published=True,
        )
        client.login(username="testuser", password="pass")
        response = client.post(
            f"/api/rate-blog-post/{post.id}/",
            {"score": 6},
            content_type="application/json",
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestBlogFeeds:
    """Tests for RSS and Atom feeds."""

    def test_rss_feed_returns_200(self, client):
        BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
            is_published=True,
        )
        response = client.get(reverse("blog_rss_feed"))
        assert response.status_code == 200
        assert response["Content-Type"].startswith("application/rss+xml")

    def test_atom_feed_returns_200(self, client):
        BlogPost.objects.create(
            title="test",
            author=User.objects.create_user(username="author1"),
            is_published=True,
        )
        response = client.get(reverse("blog_atom_feed"))
        assert response.status_code == 200
        assert response["Content-Type"].startswith("application/atom+xml")

    def test_feed_excludes_unpublished(self, client):
        BlogPost.objects.create(
            title="published",
            author=User.objects.create_user(username="author1"),
            is_published=True,
        )
        BlogPost.objects.create(
            title="draft",
            author=User.objects.create_user(username="author2"),
            is_published=False,
        )
        rss = client.get(reverse("blog_rss_feed"))
        atom = client.get(reverse("blog_atom_feed"))
        for response in (rss, atom):
            assert response.status_code == 200
            assert "published" in response.content.decode()
            assert "draft" not in response.content.decode()

    def test_feed_item_fields(self, client):
        BlogPost.objects.create(
            title="آزمایش",
            summary="خلاصه",
            keywords="آموزش, سلامت",
            author=User.objects.create_user(
                username="author1",
                first_name="علی",
                last_name="کریمی",
            ),
            is_published=True,
        )
        rss = client.get(reverse("blog_rss_feed"))
        content = rss.content.decode()
        assert "آزمایش" in content
        assert "خلاصه" in content
        assert "علی کریمی" in content
        assert "آموزش" in content
        assert "سلامت" in content
