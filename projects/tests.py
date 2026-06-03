from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Project


@override_settings(ALLOWED_HOSTS=["testserver"])
class ProjectFlowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="password",
            name="Owner",
            surname="User",
        )
        self.member = User.objects.create_user(
            email="member@example.com",
            password="password",
            name="Member",
            surname="User",
        )
        self.project = Project.objects.create(
            owner=self.owner,
            name="Test project",
            description="Project description",
        )

    def test_project_list_is_public(self):
        response = self.client.get(reverse("projects:project_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test project")

    def test_owner_can_complete_project(self):
        self.client.login(email="owner@example.com", password="password")

        response = self.client.post(reverse("projects:complete_project", args=[self.project.id]))

        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, Project.CLOSED)

    def test_authenticated_user_can_toggle_favorite(self):
        self.client.login(email="member@example.com", password="password")

        response = self.client.post(reverse("projects:toggle_favorite", args=[self.project.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.member.favorites.filter(pk=self.project.pk).exists())

    def test_authenticated_user_can_toggle_participation(self):
        self.client.login(email="member@example.com", password="password")

        response = self.client.post(reverse("projects:toggle_participate", args=[self.project.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.project.participants.filter(pk=self.member.pk).exists())

