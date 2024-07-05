from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", is_superuser=True)
        self.lesson = Lesson.objects.create(
            name="test", description="test", owner=self.user
        )
        self.course = Course.objects.create(
            name="testing", description="testing", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {"name": "test", "description": "test"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        response = self.client.patch(url)
        data = {"name": "test1", "description": "test1"}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "test1")
        self.assertEqual(data.get("description"), "test1")

    def test_lesson_delete(self):
        url = reverse("materials:lessons_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.json())
        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": "test",
                    "description": "test",
                    "preview_image": None,
                    "video_link": None,
                    "course": None,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.json(), data)

    def test_add_and_delete_subscription(self):
        url = reverse("materials:subscriptions")
        data = {
            "user": self.user,
            "course": self.course.pk,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        response = self.client.post(url, data)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
