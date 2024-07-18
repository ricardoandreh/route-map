import jsonschema
from rest_framework.serializers import ModelSerializer, ValidationError

from trip.models import Route

schema = {
    "title": "Trip JSON field",
    "description": "Basic implementation",
    "type": "object",
    "required": ["origin"],
    "properties": {
        "origin": {
            "type": "object",
            "required": ["address"],
            "properties": {
                "address": {"type": "string"},
            },
        },
    },
}


class RouteSerializer(ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"

    def validate_trip(self, value):
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError as err:
            raise ValidationError(err.message)

        return value
