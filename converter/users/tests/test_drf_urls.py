import pytest
from django.urls import resolve, reverse

from converter.users.models import User

pytestmark = pytest.mark.django_db


def test_user_detail(user: User):
    assert (
        reverse("api:user-detail", kwargs={"username": user.username})
        == f"/api/users/{user.username}/"
    )
    assert resolve(f"/api/users/{user.username}/").view_name == "api:user-detail"


def test_user_list():
    assert reverse("api:user-list") == "/api/users/"
    assert resolve("/api/users/").view_name == "api:user-list"


def test_user_me():
    assert reverse("api:user-me") == "/api/users/me/"
    assert resolve("/api/users/me/").view_name == "api:user-me"


def test_token_obtain_pair():
    assert reverse("users:token_obtain_pair") == "/users/api/token/"
    assert resolve("/users/api/token/").view_name == "users:token_obtain_pair"


def test_token_refresh():
    assert reverse("users:token_refresh") == "/users/api/token/refresh/"
    assert resolve("/users/api/token/refresh/").view_name == "users:token_refresh"


def test_create():
    assert reverse("users:create") == "/users/api/create/"
    assert resolve("/users/api/create/").view_name == "users:create"
