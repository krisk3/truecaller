"""
Define Database Models.
"""

from django.db import models
from django.conf import settings


class Contact(models.Model):
    """
    Define a Contact model.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=50)
    contact_phone = models.CharField(max_length=25)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        """
        Define how Contact object is displayed in the django admin panel.
        """
        return f"{self.contact_phone} - {self.contact_name}"


class SpamContact(models.Model):
    """
    Define a SpamContact model.
    """

    spam_phone = models.CharField(max_length=20, unique=True)
    spammed_by_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="spammed_numbers"
    )

    @property
    def spam_count(self):
        return self.spammed_by_users.count()

    class Meta:
        verbose_name = "Spam Contact"
        verbose_name_plural = "Spam Contacts"

    def __str__(self):
        """
        Define how SpamContact object is displayed in the django admin panel.
        """
        return f"{self.spam_phone} - {self.spam_count}"
