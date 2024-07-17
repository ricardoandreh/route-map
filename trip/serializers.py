from rest_framework.serializers import ModelSerializer

from trip.models import Route


class RouteSerializer(ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"
