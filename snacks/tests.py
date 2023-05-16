from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass"
        )

        self.snack = Snack.objects.create(
            name="snack", description="description test", purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "snack")

    def test_movie_content(self):
        self.assertEqual(f"{self.snack.name}", "snack")
        self.assertEqual(f"{self.snack.purchaser}", "tester")
        self.assertEqual(f"{self.snack.description}", "description test")

    def test_movie_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "snack")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_movie_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Name of Snack: snack")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_movie_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "name": "snack2",
                "description": "test",
                "purchaser": self.user,
            }, follow=True
        )
        self.assertContains(response, "snack2")

    def test_movie_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)

