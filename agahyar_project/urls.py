from typing import List

from django.contrib import admin
from django.urls import URLPattern, include, path

urlpatterns: List[URLPattern] = [
    path("admin/", admin.site.urls),
    path("", include("services.urls")),
]
