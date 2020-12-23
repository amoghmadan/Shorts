import os
import hashlib
import binascii
from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model()

User = get_user_model()


class Service(models.Model):
    """."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    name = models.CharField(_("Name"), max_length=255)
    token = models.CharField(_("Token"), max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """."""

        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        unique_together = ("user", "name")
    
    @classmethod
    def generate_key(cls):
        """."""

        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        """."""

        return self.name

    def save(self, *args, **kwargs):
        """."""

        if not self.token:
            self.token = self.generate_key()
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
            self.minified_link = self.generate_mini_key(self.service_id, self.url)
        self.expiry_at = self.updated_at + timedelta(days=7)
        super().save(*args, **kwargs)