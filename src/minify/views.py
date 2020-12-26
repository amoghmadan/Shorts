from django.utils import timezone
from django.db import IntegrityError
from rest_framework import permissions, status, views
from rest_framework.response import Response

from .models import Service, Link
from .serializers import LinkSerializer


class PutLinkView(views.APIView):
    """."""

    serializer_class = LinkSerializer
    permission_classes = [permissions.AllowAny]

    def put(self, request, *args, **kwargs):
        """."""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.pop("token")
        expiry_days = serializer.validated_data.pop("expiry_days")

        try:
            service = Service.objects.get(token=token)
        except Service.DoesNotExist:
            return Response({"detail": "Service Not Found"}, status.HTTP_404_NOT_FOUND)
        
        expiry = timezone.now() + timezone.timedelta(expiry_days)
        try:
            link = Link.objects.get(url=serializer.validated_data["url"], service=service)
            link.expiry = expiry
            link.save()
            serializer = self.serializer_class(link)
        except Link.DoesNotExist:
            link = Link(service=service, expiry=expiry, **serializer.validated_data)
            link.save()
            serializer = self.serializer_class(link)
            return Response(serializer.data, status.HTTP_201_CREATED)
        
        return Response(serializer.data, status.HTTP_200_OK)
