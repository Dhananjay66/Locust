from django.test import TestCase
from django.contrib.auth.models import User


class AuthTests(TestCase):
    def setUp(self):
        User.objects.create_user("testuser", password="testpass123")

    def test_profile_requires_login(self):
        r = self.client.get("/profile/")
        self.assertEqual(r.status_code, 401)

    def test_login_and_profile(self):
        r = self.client.post(
            "/login/",
            data={"username": "testuser", "password": "testpass123"},
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)
        r = self.client.get("/profile/")
        self.assertEqual(r.json()["username"], "testuser")