from django.contrib import admin
from users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    """Admin class for custom user."""

    list_display = ['email', 'username', ]
    search_fields = ['email', 'username', ]


admin.site.register(CustomUser, CustomUserAdmin)
