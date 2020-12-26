from django.shortcuts import redirect
from rest_framework import permissions, status, views
from rest_framework.response import Response

from minify.models import Link


class RedirectView(views.APIView):
    """."""

    model = Link
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        """."""

        try:
            link = self.model.objects.get(minified=kwargs['minified'])
        except self.model.DoesNotExist:
            return Response({"deatil": "Link Not Found"}, status.HTTP_404_NOT_FOUND)

        if timezone.now() <= link.expiry.astimezone():
            return Response({"detail": "Link Expired"}, status.HTTP_410_GONE)

        return redirect(link.url)
