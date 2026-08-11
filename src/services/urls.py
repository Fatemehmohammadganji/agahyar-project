"""URL configuration for the ``services`` application.

Maps all application routes: core pages, authentication
endpoints, bookmarks, comments, ratings, and password reset flows.
"""

from django.urls import URLPattern, path

from . import feeds, views

urlpatterns: list[URLPattern] = [
    # ===== SEO =====
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
    # ===== Core pages =====
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("search/", views.search, name="search"),
    path("service/<int:service_id>/", views.service_detail, name="service_detail"),
    path("center/<int:center_id>/", views.center_detail, name="center_detail"),
    path("services/", views.services_list, name="services_list"),
    # ===== Bookmarks =====
    path("bookmarks/", views.bookmarks_list, name="bookmarks_list"),
    path("bookmark/service/<int:service_id>/", views.set_bookmark, name="set_bookmark"),
    path(
        "bookmark/center/<int:center_id>/",
        views.set_center_bookmark,
        name="set_center_bookmark",
    ),
    # ===== Comments =====
    path(
        "comment/service/<int:service_id>/",
        views.submit_comment,
        name="submit_comment_service",
    ),
    path(
        "comment/center/<int:center_id>/",
        views.submit_comment,
        name="submit_comment_center",
    ),
    path(
        "comment/<int:comment_id>/edit/",
        views.edit_comment,
        name="edit_comment",
    ),
    path(
        "comment/<int:comment_id>/delete/",
        views.delete_comment,
        name="delete_comment",
    ),
    # ===== Blog =====
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<str:slug>/preview/", views.blog_preview, name="blog_preview"),
    path("blog/<str:slug>/", views.blog_detail, name="blog_detail"),
    path("blog/feed/rss/", feeds.BlogRssFeed(), name="blog_rss_feed"),
    path("blog/feed/atom/", feeds.BlogAtomFeed(), name="blog_atom_feed"),
    path(
        "comment/blog/<int:blog_post_id>/",
        views.submit_comment,
        name="submit_comment_blog_post",
    ),
    path(
        "api/rate-blog-post/<int:post_id>/",
        views.rate_blog_post,
        name="rate_blog_post",
    ),
    path(
        "api/ckeditor-upload/",
        views.ckeditor_upload,
        name="ckeditor_upload",
    ),
    # ===== Center ratings =====
    path(
        "rate-center/<int:center_id>/",
        views.submit_center_rating,
        name="submit_center_rating",
    ),
    path(
        "api/rate-center/<int:center_id>/",
        views.rate_center,
        name="rate_center",
    ),
    # ===== Reports =====
    path("api/report/", views.submit_report, name="submit_report"),
    # ===== Geolocation API =====
    path(
        "api/suggest-center/<int:service_id>/",
        views.suggest_closest_center,
        name="suggest_closest_center",
    ),
    path(
        "api/load-centers/<int:service_id>/",
        views.load_centers,
        name="load_centers",
    ),
    path(
        "api/load-comments/<str:target_type>/<int:target_id>/",
        views.load_comments,
        name="load_comments",
    ),
    path("api/cities/", views.cities_api, name="cities_api"),
    # ===== Supplementary pages =====
    path("profile/", views.profile_view, name="profile"),
    path("faq/", views.faq_view, name="faq"),
    path("nearby-centers/", views.nearby_centers_view, name="nearby_centers"),
    path("users/", views.show_users, name="show_users"),
    # ===== Informational pages =====
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    # ===== Authentication =====
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("verify-otp/", views.verify_otp_view, name="verify_otp"),
    path(
        "verify-profile-otp/", views.verify_profile_otp_view, name="verify_profile_otp"
    ),
    path("resend-otp/", views.resend_otp_view, name="resend_otp"),
    path("api/resend-otp/", views.resend_otp_api, name="resend_otp_api"),
    path(
        "api/resend-profile-otp/",
        views.resend_profile_otp_api,
        name="resend_profile_otp_api",
    ),
    path("logout/", views.logout_view, name="app_logout"),
    path("theme/toggle/", views.theme_toggle_view, name="theme_toggle"),
    # ===== Password reset (phone) =====
    path(
        "password-reset-phone/",
        views.password_reset_phone_view,
        name="password_reset_phone",
    ),
    path(
        "verify-password-reset-otp/",
        views.verify_password_reset_otp_view,
        name="verify_password_reset_otp",
    ),
    path(
        "api/resend-password-reset-otp/",
        views.resend_password_reset_otp_api,
        name="resend_password_reset_otp_api",
    ),
    path(
        "set-new-password/",
        views.set_new_password_view,
        name="set_new_password",
    ),
    path(
        "password-reset-phone/done/",
        views.password_reset_phone_done_view,
        name="password_reset_phone_done",
    ),
    # ===== Password reset (email) =====
    # The email flow returns 404 and its links are hidden until the admin
    # configures a real sending mail backend (see is_email_setup()).
    path("password-reset/", views.EmailResetView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        views.EmailResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.EmailResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.EmailResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
