import pytest
from django.test import Client
from django.contrib.auth.models import User
from services.models import UserProfile
from services.views import save_user_profile


@pytest.mark.django_db
class TestSaveUserProfile:

    def test_creates_new_profile(self):
        user = User.objects.create_user("newuser", password="pass12345")
        save_user_profile(user.id, "tehran", "saadatabad", "09121234567")
        profile = UserProfile.objects.get(user=user)
        assert profile.city == "tehran"
        assert profile.neighborhood == "saadatabad"
        assert profile.phone == "09121234567"

    def test_updates_existing_profile(self):
        user = User.objects.create_user("existing", password="pass12345")
        UserProfile.objects.create(user=user, city="esfahan", neighborhood="", phone="")
        save_user_profile(user.id, "tehran", "vanak", "09981234567")
        profile = UserProfile.objects.get(user=user)
        assert profile.city == "tehran"
        assert profile.neighborhood == "vanak"
        assert profile.phone == "09981234567"


@pytest.mark.django_db
class TestShowUsersView:

    def test_requires_login(self):
        client = Client()
        response = client.get("/users/")
        assert response.status_code == 302

    def test_shows_users_with_profiles(self):
        user = User.objects.create_user("viewer", password="pass12345")
        UserProfile.objects.create(user=user, city="tehran", phone="09121234567")
        client = Client()
        client.login(username="viewer", password="pass12345")
        response = client.get("/users/")
        assert response.status_code == 200
        assert "viewer" in str(response.content)
