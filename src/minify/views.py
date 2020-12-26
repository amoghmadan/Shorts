from django import views
from django.shortcuts import redirect
from rest_framework import viewsets

from .models import Service, Link
from .serializers import ServiceSerializer, LinkSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """."""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class LinkViewSet(viewsets.ModelViewSet):
    """."""

    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class RedirectView(views.View):
    """."""

    model = Link

    def get(self, request, *args, **kwargs):
        """."""

        link = Link.objects.get(minified=kwargs['minified'])
        return redirect(link.url)
