from django.utils import timezone
from rest_framework import serializers

from .models import Service, Link


class ServiceSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        """."""

        model = Service
        exclude = ("user", )
        extra_kwargs = {
            "token": {"read_only": True}
        }


class LinkSerializer(serializers.ModelSerializer):
    """."""

    token = serializers.CharField(write_only=True)
    expiry_days = serializers.IntegerField(write_only=True, min_value=1, default=7)

    class Meta:
        """."""

        model = Link
        exclude = ("service", )
        extra_kwargs = {
            "minified": {"read_only": True},
            "expiry": {"read_only": True}
        }
