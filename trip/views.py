from django.http import HttpResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from trip.models import Route
from trip.serializers import RouteSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def create(self, request, *args, **kwargs):
        if (
            "origin" not in request.data["trip"]
            or "address" not in request.data["trip"]["origin"]
        ):
            return HttpResponse(
                '"address" in "origin" field in Trip is required',
                status=status.HTTP_400_BAD_REQUEST,
            )

        print("testing")

        return super().create(request, *args, **kwargs)
