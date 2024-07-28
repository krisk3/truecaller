"""
Configure models to be managed via django admin panel.
"""

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    """
    Define admin panel page for custom user model.
    """

    ordering = ["id"]
    list_display = ["phone", "name"]
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (("Personal Info"), {"fields": ("name", "email")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            ("Important dates"),
            {
                "fields": (
                    "created_at",
                    "modified_at",
                )
            },
        ),
    )
    readonly_fields = [
        "created_at",
        "modified_at",
    ]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "name",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
