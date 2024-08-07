from django.http import HttpResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from trip.models import Route
from trip.serializers import RouteSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
