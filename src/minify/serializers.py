from rest_framework import serializers
from .models import Service, Link


class ServiceSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        """."""

        model = Service
        fields = "__all__"
        extra_kwargs = {
            "token": {
                "read_only": True
            }
        }


class LinkSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        """."""

        model = Link
        fields = "__all__"
        extra_kwargs = {
            "minified": {
                "read_only": True
            },
            "expiry": {
                "read_only": True
            }
        }
