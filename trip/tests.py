from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.test import APITestCase

from trip.models import Route
from trip.serializers import RouteSerializer


class RouteTests(APITestCase):
    def setUp(self):
        self.url = reverse("route-list")
        self.user = User.objects.create(
            username="rick",
            email="rick@email.com",
            password=make_password("strongpass123")
        )

    def test_list_empty_route(self):
        """
        Ensure we can list a empty route object.
        """
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_all_routes(self):
        """
        Ensure we can list all route objects.
        """
        Route.objects.create(user=self.user, trip='{"test", 1}')
        Route.objects.create(user=self.user, trip='{"test", 2}')
        Route.objects.create(user=self.user, trip='{"test", 3}')
        Route.objects.create(user=self.user, trip='{"test", 4}')
        response = self.client.get(self.url, format="json")
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data, serializer.data)


    def test_create_route(self):
        """
        Ensure we can create a route object.
        """
        data = {
            "user": self.user.id,
            "trip": {
                "origin": {
                    "address" : "6633+Hollywood+Boulevard",
                },
                "destination": {
                    "address" : "234+Vine+Street",
                },
                "intermediates": [
                    {"address": "204+Marshall+Road"},
                    {"address": "31+West+Street"},
                    {"address": "776+Miracle+Mile"},
                ],
                "travelMode": "DRIVE",
                "routingPreference": "TRAFFIC_AWARE",
            },
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Route.objects.get().trip["origin"]["address"], "6633+Hollywood+Boulevard")
