import os
import hashlib
import binascii

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


def generate_key():
        """."""

        return binascii.hexlify(os.urandom(20)).decode()


class Service(models.Model):
    """."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    name = models.CharField(_("Name"), max_length=255)
    token = models.CharField(_("Token"), max_length=40, default=generate_key)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """."""

        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        unique_together = ("user", "name")

    def __str__(self):
        """."""

        return self.name

    def save(self, *args, **kwargs):
        """."""

        super().save(*args, **kwargs)


class Link(models.Model):
    """."""

    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name=_("Service"))
    url = models.TextField(_("URL"))
    minified = models.CharField(_("Minified"), max_length=8, unique=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)
    expiry = models.DateTimeField(_("Expiry"))

    class Meta:
        """."""

        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    @staticmethod
    def generate_mini_key(service_id, url):
        """."""

        text = str(service_id) + ":" + url
        return hashlib.sha256(text.encode()).hexdigest()[:8]

    def __str__(self):
        """."""

        return self.url

    def save(self, *args, **kwargs):
        """."""

        if not self.minified:
            self.minified = self.generate_mini_key(self.service_id, self.url)
        super().save(*args, **kwargs)
