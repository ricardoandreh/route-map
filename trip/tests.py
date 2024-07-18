from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.test import APITestCase

from trip.models import Route
from trip.serializers import RouteSerializer


class RouteTests(APITestCase):
    def setUp(self):
        self.url = reverse("route-list")
        self.user = User.objects.create(
            username="rick",
            email="rick@email.com",
            password=make_password("strongpass123"),
        )
        self.base_data = {
            "user": self.user.id,
            "trip": {
                "origin": {
                    "address": "6633+Hollywood+Boulevard",
                },
                "destination": {
                    "address": "234+Vine+Street",
                },
                "travelMode": "DRIVE",
                "routingPreference": "TRAFFIC_AWARE",
            },
        }

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
        Route.objects.create(user=self.user, trip='{"origin", {"address": "test 1"} }')
        Route.objects.create(user=self.user, trip='{"origin", {"address": "test 2"} }')
        Route.objects.create(user=self.user, trip='{"origin", {"address": "test 3"} }')
        Route.objects.create(user=self.user, trip='{"origin", {"address": "test 4"} }')
        response = self.client.get(self.url, format="json")
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data, serializer.data)

    def test_json_trip_schema(self):
        """
        Ensure we can only maintain a trip field with the right JSON schema.
        """
        data = self.base_data
        del data["trip"]["origin"]["address"]

        with self.assertRaisesMessage(
            serializers.ValidationError, "'address' is a required property"
        ):
            serializer = RouteSerializer(data=data)
            serializer.is_valid(raise_exception=True)

        del data["trip"]["origin"]

        with self.assertRaisesMessage(
            serializers.ValidationError, "'origin' is a required property"
        ):
            serializer = RouteSerializer(data=data)
            serializer.is_valid(raise_exception=True)

    def test_create_route(self):
        """
        Ensure we can create a route object.
        """
        response = self.client.post(self.url, self.base_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Route.objects.get().trip["origin"]["address"], "6633+Hollywood+Boulevard"
        )
