"""
Configure models to be managed via django admin panel.
"""

from django.contrib import admin
from .models import Contact, SpamContact

admin.site.register(SpamContact)
admin.site.register(Contact)
