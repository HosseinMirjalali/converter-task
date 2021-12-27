from unittest import TestCase

import pytest
from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from converter.users.api.views import UserViewSet
from converter.users.models import User

pytestmark = pytest.mark.django_db

CREATE_USER_URL = reverse("users:create")


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        assert response.data == {
            "username": user.username,
            "name": user.name,
            "convert_min_left": 1000,
        }


class TestUserAPIViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_create_user_valid_data(self):
        """
        test users can be created through the "create" endpoint with valid data
        """
        payload = {
            "username": "foo",
            "password": "testpassword",
            "name": "test_name",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        assert res.status_code == status.HTTP_201_CREATED
        user = User.objects.get(**res.data)
        assert user.check_password(payload["password"])
        assert "password" not in res.data

    def test_api_create_user_missing_data(self):
        """
        test users can be created through the "create" endpoint with missing data payload (username)
        """
        payload = {
            "password": "testpassword",
            "name": "test_name",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
