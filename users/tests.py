from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserFlowTests(TestCase):
    def test_register_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "name": "New",
                "surname": "User",
                "email": "new@example.com",
                "password": "password",
            },
        )

        self.assertRedirects(response, "/projects/list/")
        self.assertTrue(get_user_model().objects.filter(email="new@example.com").exists())

    def test_login_rejects_wrong_password(self):
        get_user_model().objects.create_user(
            email="test@example.com",
            password="password",
            name="Test",
            surname="User",
        )

        response = self.client.post(
            reverse("users:login"),
            {"email": "test@example.com", "password": "wrong"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Неверный имейл или пароль")

    def test_profile_form_normalizes_phone(self):
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="password",
            name="Test",
            surname="User",
        )
        self.client.login(email="test@example.com", password="password")

        self.client.post(
            reverse("users:edit_profile"),
            {
                "name": "Test",
                "surname": "User",
                "about": "",
                "phone": "89000000000",
                "github_url": "https://github.com/test",
            },
        )

        user.refresh_from_db()
        self.assertEqual(user.phone, "+79000000000")

